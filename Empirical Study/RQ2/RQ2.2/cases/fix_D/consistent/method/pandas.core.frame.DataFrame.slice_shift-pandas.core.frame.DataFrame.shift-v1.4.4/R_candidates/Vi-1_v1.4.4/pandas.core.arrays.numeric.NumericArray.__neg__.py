    def __neg__(self):
        return type(self)(-self._data, self._mask.copy())
