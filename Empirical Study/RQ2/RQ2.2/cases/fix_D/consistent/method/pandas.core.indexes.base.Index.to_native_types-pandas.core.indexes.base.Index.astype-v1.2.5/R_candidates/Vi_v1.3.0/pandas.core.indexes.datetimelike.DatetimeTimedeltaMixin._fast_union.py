    def _fast_union(self: _T, other: _T, sort=None) -> _T:
        if len(other) == 0:
            return self.view(type(self))

        if len(self) == 0:
            return other.view(type(self))

        # to make our life easier, "sort" the two ranges
        if self[0] <= other[0]:
            left, right = self, other
        elif sort is False:
            # TDIs are not in the "correct" order and we don't want
            #  to sort but want to remove overlaps
            left, right = self, other
            left_start = left[0]
            loc = right.searchsorted(left_start, side="left")
            # error: Slice index must be an integer or None
            right_chunk = right._values[:loc]  # type: ignore[misc]
            dates = concat_compat((left._values, right_chunk))
            # With sort being False, we can't infer that result.freq == self.freq
            # TODO: no tests rely on the _with_freq("infer"); needed?
            result = type(self)._simple_new(dates, name=self.name)
            result = result._with_freq("infer")
            return result
        else:
            left, right = other, self

        left_end = left[-1]
        right_end = right[-1]

        # concatenate
        if left_end < right_end:
            loc = right.searchsorted(left_end, side="right")
            # error: Slice index must be an integer or None
            right_chunk = right._values[loc:]  # type: ignore[misc]
            dates = concat_compat([left._values, right_chunk])
            # The can_fast_union check ensures that the result.freq
            #  should match self.freq
            dates = type(self._data)(dates, freq=self.freq)
            result = type(self)._simple_new(dates)
            return result
        else:
            return left
