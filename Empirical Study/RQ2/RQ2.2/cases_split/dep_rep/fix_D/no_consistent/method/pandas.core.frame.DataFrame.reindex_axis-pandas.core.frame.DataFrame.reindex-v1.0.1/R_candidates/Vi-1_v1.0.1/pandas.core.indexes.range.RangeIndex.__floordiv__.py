    @unpack_zerodim_and_defer("__floordiv__")
    def __floordiv__(self, other):

        if is_integer(other) and other != 0:
            if len(self) == 0 or self.start % other == 0 and self.step % other == 0:
                start = self.start // other
                step = self.step // other
                stop = start + len(self) * step
                new_range = range(start, stop, step or 1)
                return self._simple_new(new_range, name=self.name)
            if len(self) == 1:
                start = self.start // other
                new_range = range(start, start + 1, 1)
                return self._simple_new(new_range, name=self.name)
        return self._int64index // other
