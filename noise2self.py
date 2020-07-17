#!/usr/bin/env python
import contextlib
import time

import numpy as np
import dask.array as da


@contextlib.contextmanager
def perf_timer(name: str):
    start_ns = time.perf_counter_ns()
    yield
    end_ns = time.perf_counter_ns()
    ms = (end_ns - start_ns) / 1e6
    print(f"{name} {ms}ms")


def da_stack(count):
    return da.stack([da.random.random((28, 28)) for i in range(count)])


def np_array(count):
    return np.array(da_stack(count))


def test_access(label, stack):
    for i in range(3):
        with perf_timer(f"    {label}[{i}] ="):
            np.asarray(stack[i])


for size in [100, 1000, 10000, 100000]:
    print(f"Size {size}")
    test_access("da_stack", da_stack(size))
    test_access("np_array", np_array(size))

"""
Sample Run

Size 100
    da_stack[0] = 9.646658ms
    da_stack[1] = 1.601273ms
    da_stack[2] = 1.35383ms
    np_array[0] = 0.002925ms
    np_array[1] = 0.001711ms
    np_array[2] = 0.001122ms
Size 1000
    da_stack[0] = 10.424023ms
    da_stack[1] = 4.408225ms
    da_stack[2] = 4.191567ms
    np_array[0] = 0.005845ms
    np_array[1] = 0.001715ms
    np_array[2] = 0.001111ms
Size 10000
    da_stack[0] = 50.034623ms
    da_stack[1] = 47.766893ms
    da_stack[2] = 48.259741ms
    np_array[0] = 0.010017ms
    np_array[1] = 0.002644ms
    np_array[2] = 0.001602ms
Size 100000
    da_stack[0] = 1001.979783ms
    da_stack[1] = 947.75337ms
    da_stack[2] = 936.373431ms
    np_array[0] = 0.011248ms
    np_array[1] = 0.002532ms
    np_array[2] = 0.00151ms
"""
