from typing import Tuple
import numpy as np

_QUAD = np.array(
    [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 0, 0], [1, 1, 0], [0, 1, 0]],
    dtype=np.float32,
)


# TODO_OCTREE: this class is placeholder, needs work
class OctreeChunk:
    """One chunk of the full image.

    A chunk is a 2D tile or a 3D sub-volume.

    Parameters
    ----------
    data : ArrayLike
        The data to draw for this chunk.
    pos : Tuple[float, float]
        The x, y coordinates of the chunk.
    size : float
        The size of the chunk, the chunk is square/cubic.
    """

    def __init__(
        self,
        level_index: int,
        data,
        pos: Tuple[float, float],
        scale: Tuple[float, float],
    ):
        # We need level_index because id(data) is sometimes duplicated in
        # adjacent layers, somehow. But it makes sense to include it
        # anyway, it's an important aspect of the chunk.
        self.level_index = level_index
        self.data = data
        self.pos = pos
        self.scale = scale

    @property
    def key(self):
        return (self.pos[0], self.pos[1], self.level_index)


def _quad(octree_chunk: OctreeChunk):
    shape = octree_chunk.data.shape

    scale = np.array(octree_chunk.scale, dtype=np.float32)

    quad = _QUAD.copy()
    quad[:, :2] *= shape * scale
    quad[:, :2] += octree_chunk.pos

    return quad


def main():
    data = np.zeros((500, 100))
    pos = (50, 10)
    scale = (5, 2)
    octree_chunk = OctreeChunk(0, data, pos, scale)

    quad = _quad(octree_chunk)
    print(quad)


if __name__ == '__main__':
    main()
