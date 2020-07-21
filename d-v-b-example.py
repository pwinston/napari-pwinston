import os

os.environ['NAPARI_ASYNC'] = '1'
import napari
import dask.array as da
import time
import random

data = da.random.randint(0, 255, (100,) * 3, chunks=(10,) * 3, dtype='uint8')


def func(v):
    # return input after a delay
    time.sleep(random.random())
    return v


data2 = data.map_blocks(func)
data_computed = data.compute()

with napari.gui_qt():
    v = napari.Viewer()
    v.add_image(data)
    v.add_image(data2)
    v.add_image(data_computed)
