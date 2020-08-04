import numpy as np
import h5py
import dask.array as da

filename = '/Users/pbw/data/sample_A/sample_A_20160501.hdf'
source_data = h5py.File(filename, 'r')
raw = np.asarray(source_data['volumes/raw'])
labels = np.asarray(source_data['volumes/labels/neuron_ids'])

raw_dask = da.from_array(raw, chunks=(1, 1250, 1250))
da.to_zarr(raw_dask, 'raw.zarr')
labels_dask = da.from_array(labels, chunks=(1, 1250, 1250))
da.to_zarr(labels_dask, 'labels.zarr')
