"""Testing reading zarr file with zarr vs. dask."""
import random
import subprocess
import time
from contextlib import contextmanager

import click
import dask.array as da
import numpy as np

import zarr


@contextmanager
def time_block(label: str) -> None:
    start = time.perf_counter_ns()
    result = {"elapsed_ms": 0}
    yield result
    elapsed_ms = (time.perf_counter_ns() - start) / 1e6
    result["elapsed_ms"] = elapsed_ms
    print(f"{elapsed_ms:6.3f}ms - {label}")


def test_reads(label, array, level):
    rows, cols = array.shape[-2:]
    for i in range(5):
        r = random.randint(0, rows - 1)
        c = random.randint(0, cols - 1)
        with time_block(f"level[{level}][{r}, {c}]"):
            np.asarray(array[0, 0, 0, r, c])
    print(f"  shape {array.shape}")


def compute_average_read(array, level):
    rows, cols = array.shape[-2:]
    count = 100
    total = 0.0
    for i in range(count):
        r = random.randint(0, rows - 1)
        c = random.randint(0, cols - 1)
        with time_block(f"level[{level}][{r}, {c}]") as result:
            np.asarray(array[0, 0, 0, r, c])
        total += result['elapsed_ms']
    return total / count


def test_zarr(path, level):
    with time_block("zarr.convenience.open"):
        infile = zarr.convenience.open(path)
    array = infile[level]
    test_reads("zarr", array, level)


def test_dask(path, level, chunks):
    with time_block("da.from_zarr"):
        array = da.from_zarr(path, level, chunks=chunks)
    test_reads("dask", array, level)


def test_both(path, method, chunks):
    for level in [7, 0]:
        print(f"\n{method} level {level} - {path}:")
        if method == "zarr":
            test_zarr(path, level)
        elif method == "dask":
            test_dask(path, level, chunks)
        else:
            ValueError(f"Unknown method {method}")


def test_average_read(path, chunks):
    level = 0
    array = da.from_zarr(path, level, chunks=chunks)
    return compute_average_read(array, level)


@click.command()
@click.argument('path', required=True)
@click.argument('method', required=True)
@click.option('--chunks', default=1024, help='Chunk size for dask')
def main(path, method, chunks):

    results = []
    # test_both(path, method, chunks)
    sizes = [2 ** x for x in range(10, 33)]
    for chunks in sizes:
        print(f"Testing chunks={chunks}")
        average_ms = test_average_read(path, chunks)
        results.append((chunks, average_ms))
        subprocess.run(["purge"])

    print("Results (chunks, milliseconds)")
    for chunks, ms in results:
        print(f"{chunks}, {ms:.3f}")


if __name__ == '__main__':
    main()
