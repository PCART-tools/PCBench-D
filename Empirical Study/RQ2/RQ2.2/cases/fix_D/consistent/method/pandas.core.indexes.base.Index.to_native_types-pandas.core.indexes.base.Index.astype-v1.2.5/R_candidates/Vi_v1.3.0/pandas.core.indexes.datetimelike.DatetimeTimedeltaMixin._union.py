    def _union(self, other, sort):
        # We are called by `union`, which is responsible for this validation
        assert isinstance(other, type(self))
        assert self.dtype == other.dtype

        if self._can_fast_union(other):
            result = self._fast_union(other, sort=sort)
            # in the case with sort=None, the _can_fast_union check ensures
            #  that result.freq == self.freq
            return result
        else:
            i8self = Int64Index._simple_new(self.asi8)
            i8other = Int64Index._simple_new(other.asi8)
            i8result = i8self._union(i8other, sort=sort)
            result = type(self)(i8result, dtype=self.dtype, freq="infer")
            return result
