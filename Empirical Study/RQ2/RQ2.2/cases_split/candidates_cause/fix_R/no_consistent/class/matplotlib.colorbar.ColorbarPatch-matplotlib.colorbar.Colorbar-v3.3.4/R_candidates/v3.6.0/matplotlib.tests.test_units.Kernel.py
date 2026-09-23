class Kernel:
    def __init__(self, array):
        self._array = np.asanyarray(array)

    def __array__(self):
        return self._array

    @property
    def shape(self):
        return self._array.shape
