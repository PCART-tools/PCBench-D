    def __floordiv__(self, other):
        if isinstance(other, (ABCSeries, ABCDataFrame)):
            return NotImplemented

        if is_integer(other) and other != 0:
            if (len(self) == 0 or
                    self._start % other == 0 and
                    self._step % other == 0):
                start = self._start // other
                step = self._step // other
                stop = start + len(self) * step
                return RangeIndex._simple_new(
                    start, stop, step, name=self.name)
            if len(self) == 1:
                start = self._start // other
                return RangeIndex._simple_new(
                    start, start + 1, 1, name=self.name)
        return self._int64index // other
