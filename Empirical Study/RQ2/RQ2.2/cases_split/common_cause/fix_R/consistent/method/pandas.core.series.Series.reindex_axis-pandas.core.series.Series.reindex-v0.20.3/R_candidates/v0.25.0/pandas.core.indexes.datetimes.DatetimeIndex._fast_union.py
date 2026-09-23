    def _fast_union(self, other, sort=None):
        if len(other) == 0:
            return self.view(type(self))

        if len(self) == 0:
            return other.view(type(self))

        # Both DTIs are monotonic. Check if they are already
        # in the "correct" order
        if self[0] <= other[0]:
            left, right = self, other
        # DTIs are not in the "correct" order and we don't want
        # to sort but want to remove overlaps
        elif sort is False:
            left, right = self, other
            left_start = left[0]
            loc = right.searchsorted(left_start, side="left")
            right_chunk = right.values[:loc]
            dates = _concat._concat_compat((left.values, right_chunk))
            return self._shallow_copy(dates)
        # DTIs are not in the "correct" order and we want
        # to sort
        else:
            left, right = other, self

        left_end = left[-1]
        right_end = right[-1]

        # TODO: consider re-implementing freq._should_cache for fastpath

        # concatenate dates
        if left_end < right_end:
            loc = right.searchsorted(left_end, side="right")
            right_chunk = right.values[loc:]
            dates = _concat._concat_compat((left.values, right_chunk))
            return self._shallow_copy(dates)
        else:
            return left
