#!/usr/bin/env python
"""
Launch napari with various datasets for development/testing/debug.

USAGE: nap.py <dataset>

Example: nap.py small
"""
import os
import sys
import time

import dask
import dask.array as da
import numpy as np

from text_image import create_text_array


DATASETS = {}

ENV = {"NAPARI_PERFMON": "1", "NAPARI_ASYNC_LOAD": "1"}


def _dump_env():
    for key, value in os.environ.items():
        if key.startswith("NAPARI"):
            print(key, value)


def add_delay(array, seconds):
    @dask.delayed
    def delayed(array):
        time.sleep(seconds)
        return array

    return da.from_delayed(delayed(array), array.shape, array.dtype)


def run_napari(usage=False):
    def numbered_delayed():
        @dask.delayed
        def image(x):
            time.sleep(1)
            return create_text_array(x)

        images = [
            da.from_delayed(image(x), (1024, 1024), dtype=float)
            for x in range(20)
        ]
        data = np.stack(images, axis=0)
        return napari.view_image(data, name='delayed (1 second)')

    def create_images(nx, ny, count, seconds):
        @dask.delayed
        def image(x):
            time.sleep(1)
            return create_text_array(x)

        return [
            da.from_delayed(image(x), (1024, 1024), dtype=float)
            for x in range(20)
        ]
        return [
            add_delay(create_text_array(x, nx, ny), seconds)
            for x in range(count)
        ]

    def numbered_4():
        count = 20
        seconds = 1
        images = [
            np.stack(create_images(0.25, 0.25, count, seconds), axis=0),
            np.stack(create_images(0.75, 0.25, count, seconds), axis=0),
            np.stack(create_images(0.25, 0.75, count, seconds), axis=0),
            np.stack(create_images(0.75, 0.75, count, seconds), axis=0),
        ]
        # images = create_images(0.50, 0.5, 20, seconds)
        data = np.stack(images, axis=0)
        return napari.view_image(data, name='numbered slices', channel_axis=0)

    def numbered2():
        data = add_delay(np.array(create_text_array("one")), 1)
        return napari.view_image(data, name='numbered slices', channel_axis=0)

    def numbered():
        images = [create_text_array(x) for x in range(20)]
        data = np.stack(images, axis=0)
        return napari.view_image(data, name='numbered slices')

    def invisible():
        return napari.view_image(
            np.random.random((5, 1024, 1024)),
            name='five 1k images',
            visible=False,
        )

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

    def small3d():
        return napari.view_image(
            np.random.random((3, 64, 64, 64)),
            ndisplay=3,
            name='small 3D timeseries',
        )

    def labels():
        return napari.view_labels(
            np.random.randint(10, size=(20, 2048, 2048)),
            name='big labels timeseries',
        )

    DATASETS = {
        "numbered_delayed": numbered_delayed,
        "numbered": numbered,
        "numbered_4": numbered_4,
        "numbered2": numbered2,
        "invisible": invisible,
        "noise": noise,
        "big8": big8,
        "big16": big16,
        "big2d": big2d,
        "big3d": big3d,
        "small3d": small3d,
        "labels": labels,
        "remote": "https://s3.embassy.ebi.ac.uk/idr/zarr/v0.1/4495402.zarr",
        "big": "/data-ext/4495402.zarr",
        "small": "/data-local/6001240.zarr",
    }

    if usage:
        print('\n'.join(DATASETS.keys()))
        return 2

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
        run_napari(usage=True)
        sys.exit(1)

    _dump_env()
    os.environ.update(ENV)
    run_napari()
