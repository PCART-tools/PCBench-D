    def _wrap_joined_index(self, joined, other):
        name = get_op_result_name(self, other)
        if (isinstance(other, DatetimeIndex) and
                self.freq == other.freq and
                self._can_fast_union(other)):
            joined = self._shallow_copy(joined)
            joined.name = name
            return joined
        else:
            tz = getattr(other, 'tz', None)
            return self._simple_new(joined, name, tz=tz)
