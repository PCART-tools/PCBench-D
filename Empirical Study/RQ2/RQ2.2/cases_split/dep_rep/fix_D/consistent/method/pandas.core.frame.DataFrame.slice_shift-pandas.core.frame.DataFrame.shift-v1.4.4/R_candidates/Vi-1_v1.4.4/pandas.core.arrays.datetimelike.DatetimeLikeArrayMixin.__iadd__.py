    def __iadd__(self, other):
        result = self + other
        self[:] = result[:]

        if not is_period_dtype(self.dtype):
            # restore freq, which is invalidated by setitem
            self._freq = result.freq
        return self
