    def __neg__(self):
        if self.freq is not None:
            return type(self)(-self._data, freq=-self.freq)
        return type(self)(-self._data)
