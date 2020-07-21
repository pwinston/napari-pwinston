import os

import dask.array as da
import time
import random
import threading
import numpy as np

data = da.random.randint(0, 255, (100,) * 3, chunks=(10,) * 3, dtype='uint8')


class Tracker:
    def __init__(self):
        self.thread_num = 0
        self.count = 0
        self.map = {}

    def start(self):
        self.thread_num = 0
        self.count = 0
        self.map = {}
        self.start_time = time.time()

    def mark(self):
        self.count += 1
        ident = threading.get_ident()
        try:
            return self.map[ident]
        except KeyError:
            self.map[ident] = self.thread_num
            self.thread_num += 1
            return self.map[ident]

    def done(self):
        seconds = time.time() - self.start_time
        print(f"Calls: {self.count}")
        print(f"Threads: {self.thread_num}")
        print(f"Time: {seconds} seconds.")


tracker = Tracker()


def func(v):
    delay = random.random()
    print(f"{tracker.mark()} for {delay} seconds...")
    time.sleep(delay)
    return v


data2 = data.map_blocks(func)

print("START")
tracker.start()
np.asarray(data2[0, :, :])
tracker.done()

tracker.start()
np.asarray(data2[1, :, :])
tracker.done()
