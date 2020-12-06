import os
import sys
from typing import List

import dask.array as da
import napari
import numpy as np


def get_pyramid(path: str) -> List[da.Array]:
    levels = ["base"] + sorted(
        [
            s
            for s in os.listdir(path)
            if (not s.startswith(".")) and (s != "base")
        ]
    )
    return [da.from_zarr(f"{str(path)}/{level}").rechunk() for level in levels]


def main(path: str) -> None:
    pyramid = get_pyramid(path)
    print(pyramid[0][0, 0, 0])

    with napari.gui_qt():
        viewer = napari.Viewer()
        viewer.add_image(
            pyramid
        )  # [0])  # add this in to load only the base layer


if __name__ == "__main__":
    main(sys.argv[1])
