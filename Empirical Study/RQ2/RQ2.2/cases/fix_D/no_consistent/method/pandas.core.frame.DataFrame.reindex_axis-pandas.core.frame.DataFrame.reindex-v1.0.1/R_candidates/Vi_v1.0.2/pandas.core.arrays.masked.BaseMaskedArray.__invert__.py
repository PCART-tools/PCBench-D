    def __invert__(self):
        return type(self)(~self._data, self._mask)
