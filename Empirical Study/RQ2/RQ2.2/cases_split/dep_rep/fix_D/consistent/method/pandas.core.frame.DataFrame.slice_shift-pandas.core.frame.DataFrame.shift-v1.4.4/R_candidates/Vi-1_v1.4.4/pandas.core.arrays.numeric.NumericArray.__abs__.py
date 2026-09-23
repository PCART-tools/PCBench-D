    def __abs__(self):
        return type(self)(abs(self._data), self._mask.copy())
