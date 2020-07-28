"""
View 2D slices of electron microscopy data
"""
import h5py
import napari

import dask.array as da

filename = '/System/Volumes/Data/data/sample_A_20160501.hdf'
data = h5py.File(filename, 'r')
# note: import numpy as np and wrap these calls in `np.asarray()` to speed
# things up a little, but not a lot.
raw = da.from_array(data['volumes/raw'])
neuron_labels = da.from_array(data['volumes/labels/neuron_ids'])

with napari.gui_qt():
    # create an empty viewer
    viewer = napari.Viewer()

    raw_layer = viewer.add_image(raw, colormap='gray', scale=[10, 1, 1])
    neuron_labels_layer = viewer.add_labels(
        neuron_labels, opacity=0.4, scale=[10, 1, 1]
    )
