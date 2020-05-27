#
# gendata.py
#
from pathlib import Path
import sys

import click
import humanize
import numpy as np
import zarr

DATASETS = {
    "1000-chunks-0": {
        "shape": (1000, 1000),
        "chunks": None
    },

    "1000-chunks-100": {
        "shape": (1000, 1000),
        "chunks": (100, 100)
    },

    "10000-chunks-100": {
        "shape": (10000, 10000),
        "chunks": (100, 100)
    },

    "10000-chunks-1000": {
        "shape": (10000, 10000),
        "chunks": (100, 100)
    }
}

def info():
    print(zarr.storage.default_compressor)


def _directory_size_bytes(path):
    return sum(f.stat().st_size for f in path.glob("**/*") if f.is_file())


def _print_zarr_info(path):
    num_bytes = _directory_size_bytes(path)
    size_str = humanize.naturalsize(num_bytes)

    z = zarr.open(str(path), mode="r")
    num_elements = z.size
    bytes_per_elements = num_bytes / num_elements

    print(f"{path} is {num_elements} @ {bytes_per_elements} bytes each = {size_str}.")


def _random_fill_int(array, shape):
    """
    Random fill means essentially no compression.
    """
    max_int = 2 ** 31 - 1
    array[:] = np.random.randint(0, max_int, size=shape)

def _random_fill_float(array, shape):
    """
    Random fill means essentially no compression.
    """
    array[:] = np.random.rand(*shape)


def create(spec, path):
    """
    Write zarr file to disk.
    """
    # print(f"Writing {path}...")
    shape = spec["shape"]
    chunks = spec["chunks"]
    z = zarr.open(str(path), mode="w", shape=shape, chunks=chunks, dtype="f")
    _random_fill_float(z, shape)
    # print(z[:])
    _print_zarr_info(path)


def read(path):
    """
    Read to make sure it's there.
    """
    z = zarr.open(str(path), mode="r")
    print(z[:])

@click.command()
@click.argument('output_path', type=Path)
def generate(output_path):
    info()
    for name, spec in DATASETS.items():
        path = output_path / (name + ".zarr")
        create(spec, path)
        # read(path)


if __name__ == "__main__":
    sys.exit(generate())
