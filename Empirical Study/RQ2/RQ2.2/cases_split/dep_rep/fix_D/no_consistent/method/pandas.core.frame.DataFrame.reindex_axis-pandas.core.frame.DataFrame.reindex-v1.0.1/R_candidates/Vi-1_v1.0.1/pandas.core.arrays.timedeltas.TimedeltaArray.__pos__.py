    def __pos__(self):
        return type(self)(self._data, freq=self.freq)
