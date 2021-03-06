import contextlib
from time import perf_counter_ns
from typing import Optional
from collections import namedtuple
import os
import threading

# The span of time that the event ocurred.
Span = namedtuple("Span", "start_ns end_ns")

# What process/thread produced the event.
Origin = namedtuple("Origin", "process_id thread_id")


class PerfEvent:
    """A performance related event: timer, counter, etc.

    Parameters
    ----------
    name : str
        The name of this event like "draw".
    start_ns : int
        Start time in nanoseconds.
    end_ns : int
        End time in nanoseconds.
    category :str
        Comma separated categories such has "render,update".
    process_id : int
        The process id that produced the event.
    thread_id : int
        The thread id that produced the event.
    phase : str
        The Chrome Tracing "phase" such as "X", "I", "C".
    **kwargs : dict
        Additional keyword arguments for the "args" field of the event.


    Attributes
    ----------
    name : str
        The name of this event like "draw".
    span : Span
        The time span when the event happened.
    category : str
        Comma separated categories such has "render,update".
    origin : Origin
        The process and thread that produced the event.
    args : dict
        Arbitrary keyword arguments for this event.
    phase : str
        The Chrome Tracing phase (event type):
          "X" - Complete Events
          "I" - Instant Events
          "C" - Counter Events
    Notes
    -----
    The time stamps are from perf_counter_ns() and do not indicate time of
    day. The origin is arbitrary, but subtracting two counters results in a
    valid span of wall clock time. If start is the same as the end the
    event was instant.

    Google the phrase "Trace Event Format" for the full Chrome Tracing spec.
    """

    def __init__(
        self,
        name: str,
        start_ns: int,
        end_ns: int,
        category: Optional[str] = None,
        process_id: int = os.getpid(),
        thread_id: int = threading.get_ident(),
        phase: str = "X",  # "X" is a "complete event" in their spec.
        **kwargs: dict,
    ):
        self.name: str = name
        self.span: Span = Span(start_ns, end_ns)
        self.category: str = category
        self.origin: Origin = Origin(process_id, thread_id)
        self.args = kwargs
        self.phase: str = phase

    def update_end_ns(self, end_ns):
        self.span = Span(self.span.start_ns, end_ns)

    @property
    def start_us(self):
        """Start time in microseconds."""
        return self.span.start_ns / 1e3

    @property
    def start_ms(self):
        """Start time in milliseconds."""
        return self.span.start_ns / 1e6

    @property
    def duration_ns(self):
        """Duration in nanoseconds."""
        return self.span.end_ns - self.span.start_ns

    @property
    def duration_us(self):
        """Duration in microseconds."""
        return self.duration_ns / 1e3

    @property
    def duration_ms(self):
        """Duration in milliseconds."""
        return self.duration_ns / 1e6


@contextlib.contextmanager
def perf_timer(
    name: str,
    category: Optional[str] = None,
    print_time: bool = False,
    **kwargs,
):
    """Time a block of code.

    It's best to use the perfmon config file to monkey-patch this timer
    into methods an functions. However you can manually use it to time
    a block of code or even a single lines.

    Parameters
    ----------
    name : str
        The name of this timer.
    category : str
        Comma separated categories such has "render,update".
    **kwargs : dict
        Additional keyword arguments for the "args" field of the event.

    Example
    -------
    with perf_timer("draw"):
        draw_stuff()
    """
    start_ns = perf_counter_ns()

    # Intially we don't know the end_ns, but we want to yield the
    # event, so we poke in end_ns after the yield.
    event = PerfEvent(name, start_ns, start_ns, category, **kwargs)
    yield event

    # Now update the end time.
    event.update_end_ns(perf_counter_ns())

    if print_time:
        print(event.duration_ms)
