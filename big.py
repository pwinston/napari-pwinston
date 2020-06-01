#!/usr/bin/env python
import os
import sys

import numpy as np


ENV = {
    "NAPARI_PERFMON": "1",
}


def run_napari():
    import napari

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
        "big8": big8,
        "big16": big16,
        "2d": big2d,
        "3d": big3d,
        "labels": labels,
    }

    with napari.gui_qt():
        func = DATASETS[sys.argv[1]]
        viewer = func()


def usage():
    datasets = DATASETS.keys()
    datasets_str = ", ".join(datasets)
    print("USAGE: nap.py <dataset>")
    print(f"Datasets: {datasets_str}")


if __name__ == "__main__":

    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    os.environ.update(ENV)
    run_napari()
