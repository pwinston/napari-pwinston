from concurrent import futures
import sys
import time
import threading

from qtpy.QtWidgets import QApplication, QPushButton
from qtpy.QtCore import Signal, Slot, QObject


class ChunkLoaderSignals(QObject):
    finished = Signal()


class ChunkRequest:
    def __init__(self, index):
        self.index = index


def _chunk_loader_worker(request: ChunkRequest):
    ident = threading.get_ident()
    print(f"[{ident}]  ChunkLoader worker loading: {request.index}")
    time.sleep(1)
    return request


class ChunkLoader:
    NUM_WORKER_THREADS = 1

    def __init__(self):
        self.executor = futures.ThreadPoolExecutor(
            max_workers=self.NUM_WORKER_THREADS
        )
        self.futures = []
        self.signals = ChunkLoaderSignals()

    def load_chunk(self, request: ChunkRequest):
        ident = threading.get_ident()
        print(f"[{ident}] ChunkLoader.load_chunk: {request.index}")
        future = self.executor.submit(_chunk_loader_worker, request)
        future.add_done_callback(self.done)
        self.futures.append(future)
        return future

    def done(self, future):
        ident = threading.get_ident()
        request = future.result()
        print(f"[{ident}] ChunkLoader.done: {request.index}")
        self.signals.finished.emit()


CHUNK_LOADER = ChunkLoader()


class Listener(QObject):
    def __init__(self, signal):
        super().__init__()
        signal.connect(self.on_finished)
        print("Listener: connected")

    @Slot()
    def on_finished(self):
        ident = threading.get_ident()
        print(f"[{ident}] Listener")


index = 0


def func():
    print("func: requesting")
    global index
    request = ChunkRequest(index)
    index += 1
    CHUNK_LOADER.load_chunk(request)


class Application(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.listener = Listener(CHUNK_LOADER.signals.finished)


app = Application(sys.argv)
button = QPushButton("Load One Chunk")
button.clicked.connect(func)
button.show()
sys.exit(app.exec_())
