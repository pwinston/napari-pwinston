#!/usr/bin/env python
"""
Small launcher script for napari for development/testing/debug:

1) So we can give short names to datases like "big" or "remote".
2) So we can configure any env variables we want.
3) Eventually can grow to do more.
"""
import os
import sys

import numpy as np


DATASETS = {}

ENV = {
    "NAPARI_PERFMON": "1",
}


def usage():
    datasets = DATASETS.keys()
    datasets_str = ", ".join(datasets)
    print("USAGE: nap.py <dataset>")
    print(f"Datasets: {datasets_str}")


def run_napari():
    def noise():
        return napari.view_image(
            np.random.random((5, 1024, 1024)), name='five 1k images'
        )

    def big8():
        return napari.view_image(
            np.random.random((2, 8192, 8192)), name='two 8k 2d images'
        )

    def big16():
        return napari.view_image(
            np.random.random((2, 16384, 16384)), name='two 16k 2d images'
        )

    def big2d():
        return napari.view_image(
            np.random.random((21, 8192, 8192)), name='big 2D timeseries'
        )

    def big3d():
        return napari.view_image(
            np.random.random((6, 256, 512, 512)),
            ndisplay=3,
            name='big 3D timeseries',
        )

    def labels():
        return napari.view_labels(
            np.random.randint(10, size=(20, 2048, 2048)),
            name='big labels timeseries',
        )

    DATASETS = {
        "noise": noise,
        "big8": big8,
        "big16": big16,
        "2d": big2d,
        "3d": big3d,
        "labels": labels,
        "remote": "https://s3.embassy.ebi.ac.uk/idr/zarr/v0.1/4495402.zarr",
        "big": "/data-ext/4495402.zarr",
        "small": "/data-local/6001240.zarr",
    }

    name = sys.argv[1]
    data_set = DATASETS[name]

    if isinstance(data_set, str):
        # Import late so it sees our env vars.
        from napari.__main__ import main as napari_main

        print(f"LOADING {name}: {data_set}")
        sys.argv[1] = data_set
        sys.exit(napari_main())

    else:
        # Import late so it sees our env vars.
        import napari

        print(f"CREATING: {name}")

        # It's a callable function
        with napari.gui_qt():
            viewer = data_set()
            print(viewer._title)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    os.environ.update(ENV)
    run_napari()
