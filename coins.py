from skimage import data
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label
from skimage.morphology import closing, square, remove_small_objects
import napari


coins = data.coins()[50:-50, 50:-50]
# apply threshold
thresh = threshold_otsu(coins)
bw = closing(coins > thresh, square(4))
# remove artifacts connected to image border
cleared = remove_small_objects(clear_border(bw), 20)
# label image regions
label_image = label(cleared)

with napari.gui_qt():
    # create the viewer and add the coins image
    viewer = napari.view_image(coins, name='coins')
    # add the labels
    viewer.add_labels(label_image, name='segmentation')
