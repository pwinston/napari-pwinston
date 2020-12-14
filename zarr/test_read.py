import os
import random
import time
from pathlib import Path


def main():
    root = Path("/data-ext/4495402.zarr")

    for level in reversed(range(0, 7)):
        path = root / str(level)
        files = os.listdir(path)
        for i in range(5):
            index = random.randint(0, len(files))
            filename = files[index]
            start = time.time()
            filepath = path / filename
            with open(filepath, "rb") as file:
                file.read()
            ms = (time.time() - start) * 1000
            print(f"Read {filepath} in {ms:.3f}ms")


if __name__ == '__main__':
    main()
