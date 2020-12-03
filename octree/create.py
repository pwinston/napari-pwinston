import numpy
import skimage.data as data
import zarr
from skimage.transform import pyramid_gaussian


def create_zarr(
    path: str, image: numpy.ndarray, chunk_size: int = 512
) -> None:
    pyramid = pyramid_gaussian(
        image, downscale=2, max_layer=4, multichannel=True
    )

    store = zarr.DirectoryStore(path)
    with zarr.group(store, overwrite=True) as group:
        series = []
        for i, layer in enumerate(pyramid):
            path = "base" if i == 0 else f"L{i}"
            group.create_dataset(
                path, data=layer, chunks=(chunk_size, chunk_size, 3)
            )
            series.append({"path": path})

        multiscales = [
            {"name": "pyramid", "datasets": series, "type": "pyramid"}
        ]
        group.attrs["multiscales"] = multiscales


create_zarr("./image.zarr", numpy.tile(data.astronaut(), reps=(10, 10, 1)))
