    def __iadd__(self, other) -> Self:
        result = self + other
        self[:] = result[:]

        if not isinstance(self.dtype, PeriodDtype):
            # restore freq, which is invalidated by setitem
            self._freq = result.freq
        return self
