import numpy as np


class Container:
    def __init__(self, data):
        self._data = data

    @property
    def data(self):
        """array: Image data."""
        print("getter")
        return self._data

    @data.setter
    def data(self, data):
        print("setter")
        self._data = data


def main():
    data = np.random.random((10, 10))
    c = Container(data)
    c.data[0, 0] = 1


if __name__ == "__main__":
    main()

