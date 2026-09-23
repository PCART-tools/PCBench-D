    def _add_delta(self, other):
        ordinal_delta = self._maybe_convert_timedelta(other)
        return self.shift(ordinal_delta)
