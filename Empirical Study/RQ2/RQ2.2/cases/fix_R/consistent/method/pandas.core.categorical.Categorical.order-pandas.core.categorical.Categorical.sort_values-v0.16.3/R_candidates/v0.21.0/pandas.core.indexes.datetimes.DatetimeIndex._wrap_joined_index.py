    def _wrap_joined_index(self, joined, other):
        name = self.name if self.name == other.name else None
        if (isinstance(other, DatetimeIndex) and
                self.offset == other.offset and
                self._can_fast_union(other)):
            joined = self._shallow_copy(joined)
            joined.name = name
            return joined
        else:
            tz = getattr(other, 'tz', None)
            return self._simple_new(joined, name, tz=tz)
