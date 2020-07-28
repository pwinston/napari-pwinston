import numpy as np
import napari


with napari.gui_qt():
    viewer = napari.view_image(np.random.random((1024, 1024)))
    viewer.close()
    print(f"num_layers = {len(viewer.layers)}")
