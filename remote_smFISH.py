"""
Dynamically load and process data
"""

import napari
import dask.array as da
from dask_image.ndfilters import gaussian_filter
from skimage.restoration import richardson_lucy
import numpy as np


def nick():
    file_path = 's3://sofroniewn/image-data/smFISH/raw.zarr'
    raw = da.from_zarr(file_path)
    blurred = gaussian_filter(raw, (0, 2, 2))

    x, y = np.meshgrid(np.linspace(-1, 1, 6), np.linspace(-1, 1, 6))
    d = np.sqrt(x * x + y * y)
    sigma, mu = 2.0, 0.0
    psf = np.expand_dims(np.exp(-((d - mu) ** 2 / (2.0 * sigma ** 2))), axis=0)
    deconvolved = blurred.map_blocks(
        lambda block: richardson_lucy(block, psf, clip=False)
    )

    viewer = napari.Viewer()
    viewer.add_image(raw, contrast_limits=(140.0, 1200.0))
    viewer.add_image(blurred, contrast_limits=(140.0, 1200.0))
    viewer.add_image(deconvolved, contrast_limits=(140.0, 1200.0))


def talley():
    data = da.from_zarr("s3://tjl-data/neuro.zarr")
    napari.view_image(data, channel_axis=0, contrast_limits=(0, 1800))


with napari.gui_qt():
    talley()

