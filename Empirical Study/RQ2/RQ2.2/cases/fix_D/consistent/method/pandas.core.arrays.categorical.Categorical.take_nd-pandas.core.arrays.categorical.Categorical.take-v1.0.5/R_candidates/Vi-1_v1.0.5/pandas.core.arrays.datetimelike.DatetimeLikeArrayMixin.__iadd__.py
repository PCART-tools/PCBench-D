    def __iadd__(self, other):  # type: ignore
        result = self + other
        self[:] = result[:]

        if not is_period_dtype(self):
            # restore freq, which is invalidated by setitem
            self._freq = result._freq
        return self
