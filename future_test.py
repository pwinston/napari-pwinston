from concurrent import futures
import time


class ChunkRequest:
    """Ask the ChunkLoader to load this data in a worker thread.

    Placeholder class: get rid of this class if it doesn't grow!

    Parameters
    ----------
    array : ArrayLike
        Load the data from this array.
    """

    def __init__(self, request: int):
        self.request = request


def _chunk_loader_worker(request: ChunkRequest):
    time.sleep(1)
    return 42


class ChunkLoader:
    NUM_WORKER_THREADS = 3

    def __init__(self):
        self.executor = futures.ThreadPoolExecutor(
            max_workers=self.NUM_WORKER_THREADS
        )
        self.futures: FutureList = []

    def load_chunk(self, request: ChunkRequest) -> futures.Future:
        future = self.executor.submit(_chunk_loader_worker, request)
        future.add_done_callback(self.done)
        self.futures.append(future)
        return future

    def clear(self) -> None:
        """Clear queued requests that have not started loading.

        We cannot stop loads that are already in progress. We call cancel()
        on each future, but it will only cancel if it hasn't started
        already, if it hasn't been assigned to a worker thread.
        """
        before = len(self.futures)
        self.futures[:] = [x for x in self.futures if x.cancel()]
        after = len(self.futures)
        print(f"ChunkLoader.clear: {before} -> {after}")

    def done(self, future):
        print("DONE")

    def wait(self) -> bool:
        for future in self.futures:
            print(f"Result: {future.result()}")


CHUNK_LOADER = ChunkLoader()

start = time.time()
CHUNK_LOADER.load_chunk(ChunkRequest(1))
CHUNK_LOADER.load_chunk(ChunkRequest(2))
CHUNK_LOADER.load_chunk(ChunkRequest(3))
CHUNK_LOADER.load_chunk(ChunkRequest(4))
CHUNK_LOADER.load_chunk(ChunkRequest(5))
CHUNK_LOADER.wait()
elapsed = time.time() - start
print(f"Duration {elapsed}")
