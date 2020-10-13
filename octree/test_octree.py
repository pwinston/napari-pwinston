from napari import QtCore
from napari.layers.image.experimental.octree import Octree


if __name__ == "__main__":
    tree = Octree()
    print(tree.root)
    print(tree.root.children)
