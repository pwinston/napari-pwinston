import sys

import numpy as np
import skimage.data as data
import zarr
from skimage.transform import pyramid_gaussian


def create_zarr(path: str, image: np.ndarray, chunk_size: int = 512) -> None:
    print("Computing pyramid...")
    pyramid = pyramid_gaussian(
        image, downscale=2, max_layer=4, multichannel=True
    )

    # levels = list(pyramid)
    # for index, level in enumerate(levels):
    #    level = level.astype(np.uint8)
    #    print(f"index: {index} -> {level.shape} -> {level.dtype}")

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
    image = np.tile(data.astronaut(), reps=(10, 10, 1))
    print("Input shape: ", image.shape)
    print("Input dtype: ", image.dtype)
    create_zarr(path, image)


if __name__ == "__main__":
    main(sys.argv[1])
