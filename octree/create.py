import math
import sys

import numpy as np
import skimage.data as data
import zarr
from skimage.color import rgb2gray
from skimage.transform import pyramid_gaussian


def _dump_pyramid(pyramid):
    last_size = None
    for level in pyramid:
        if last_size is not None:
            downscale = math.sqrt(last_size / level.size)
            print(
                f"size={level.size} shape={level.shape} downscale={downscale}"
            )
        else:
            print(f"size={level.size} shape={level.shape}")
        last_size = level.size


def create_zarr(path: str, image: np.ndarray, chunk_size: int = 512) -> None:
    print("Computing pyramid...")
    pyramid = pyramid_gaussian(
        image, downscale=2, max_layer=4, multichannel=True
    )

    # Printer here seems to break writing the zarr file!?
    # _dump_pyramid(pyramid)

    store = zarr.DirectoryStore(path)
    with zarr.group(store, overwrite=True) as group:
        series = []
        for i, layer in enumerate(pyramid):
            layer = (255 * layer).astype(np.uint8)
            max_val = np.amax(layer)
            print(
                f"Layer {i} -> {layer.shape} -> {layer.dtype} -> max {max_val}"
            )
            path = "base" if i == 0 else f"L{i}"
            group.create_dataset(
                path, data=layer, chunks=(chunk_size, chunk_size, 3)
            )
            series.append({"path": path})

        multiscales = [
            {"name": "pyramid", "datasets": series, "type": "pyramid"}
        ]
        group.attrs["multiscales"] = multiscales


def main(path: str) -> None:
    color = data.astronaut()
    gray = rgb2gray(color)

    print(f"color.shape = {color.shape} dtype={color.dtype}")
    print(f"gray.shape = {gray.shape} dtype={color.dtype}")

    # Make it RGB but with grayscale colors. RGB is more demanding on
    # performance (bigger) but the color astronaut makes it hard to see the
    # red tile boundaries.
    color[:, :, 0] = gray[:] * 255
    color[:, :, 1] = gray[:] * 255
    color[:, :, 2] = gray[:] * 255

    image = np.tile(color, reps=(10, 10, 1))
    print("Input shape: ", image.shape)
    print("Input dtype: ", image.dtype)
    create_zarr(path, image)


if __name__ == "__main__":
    main(sys.argv[1])
