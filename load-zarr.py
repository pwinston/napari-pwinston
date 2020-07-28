import dask.array as da
import napari

labels_path = '/System/Volumes/Data/data/sample_A/labels.zarr'
image_path = '/System/Volumes/Data/data/sample_A/raw.zarr'

labels = da.from_zarr(labels_path)
image = da.from_zarr(image_path)
with napari.gui_qt():
    v = napari.Viewer()
    v.add_image(image, scale=[10, 1, 1])
    v.add_labels(labels, scale=[10, 1, 1], opacity=0.4)

