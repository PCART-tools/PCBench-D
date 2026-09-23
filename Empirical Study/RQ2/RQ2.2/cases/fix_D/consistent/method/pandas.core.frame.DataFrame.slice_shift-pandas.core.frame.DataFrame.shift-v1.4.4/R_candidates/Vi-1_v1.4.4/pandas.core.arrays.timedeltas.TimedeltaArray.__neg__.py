    def __neg__(self) -> TimedeltaArray:
        if self.freq is not None:
            return type(self)(-self._ndarray, freq=-self.freq)
        return type(self)(-self._ndarray)
