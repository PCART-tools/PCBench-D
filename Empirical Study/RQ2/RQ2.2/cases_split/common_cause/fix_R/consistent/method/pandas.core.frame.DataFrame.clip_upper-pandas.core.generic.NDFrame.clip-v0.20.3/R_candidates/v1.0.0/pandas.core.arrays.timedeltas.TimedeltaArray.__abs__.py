    def __abs__(self):
        # Note: freq is not preserved
        return type(self)(np.abs(self._data))
