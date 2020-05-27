import napari
import numpy as np

with napari.gui_qt():
    viewer = napari.view_image(
        np.random.random((21, 8192, 8192)), name='big 2D timeseries'
    )
