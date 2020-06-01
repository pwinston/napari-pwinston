#!/usr/bin/env python
"""
Small launcher script for napari for development/testing/debug:

1) So we can give short names to datases like "big" or "remote".
2) So we can configure any env variables we want.
3) Eventually can grow to do more.
"""
import os
import sys


DATASETS = {
    "remote": "https://s3.embassy.ebi.ac.uk/idr/zarr/v0.1/4495402.zarr",
    "big": "/data-ext/4495402.zarr",
    "small": "/data-local/6001240.zarr",
}

ENV = {
    "NAPARI_PERFMON": "1",
}


def usage():
    datasets = DATASETS.keys()
    datasets_str = ", ".join(datasets)
    print("USAGE: nap.py <dataset>")
    print(f"Datasets: {datasets_str}")


def run_napari():
    # We import late so any env variables we set are present
    # while napari is setting up.
    from napari.__main__ import main

    sys.argv[1] = DATASETS[sys.argv[1]]
    sys.exit(main())


if __name__ == "__main__":

    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    os.environ.update(ENV)
    run_napari()
