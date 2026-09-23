    def _wrap_joined_index(self, joined, other):
        name = get_op_result_name(self, other)
        if (
            isinstance(other, TimedeltaIndex)
            and self.freq == other.freq
            and self._can_fast_union(other)
        ):
            joined = self._shallow_copy(joined, name=name)
            return joined
        else:
            return self._simple_new(joined, name)
