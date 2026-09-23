    def __pos__(self) -> TimedeltaArray:
        return type(self)(self._ndarray.copy(), freq=self.freq)
