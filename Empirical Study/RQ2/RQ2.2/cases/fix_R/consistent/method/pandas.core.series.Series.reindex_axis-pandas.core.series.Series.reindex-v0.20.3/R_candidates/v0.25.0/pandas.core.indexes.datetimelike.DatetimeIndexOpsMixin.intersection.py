    def intersection(self, other, sort=False):
        self._validate_sort_keyword(sort)
        self._assert_can_do_setop(other)

        if self.equals(other):
            return self._get_reconciled_name_object(other)

        if len(self) == 0:
            return self.copy()
        if len(other) == 0:
            return other.copy()

        if not isinstance(other, type(self)):
            result = Index.intersection(self, other, sort=sort)
            if isinstance(result, type(self)):
                if result.freq is None:
                    result.freq = to_offset(result.inferred_freq)
            return result

        elif (
            other.freq is None
            or self.freq is None
            or other.freq != self.freq
            or not other.freq.isAnchored()
            or (not self.is_monotonic or not other.is_monotonic)
        ):
            result = Index.intersection(self, other, sort=sort)

            # Invalidate the freq of `result`, which may not be correct at
            # this point, depending on the values.
            result.freq = None
            if hasattr(self, "tz"):
                result = self._shallow_copy(
                    result._values, name=result.name, tz=result.tz, freq=None
                )
            else:
                result = self._shallow_copy(result._values, name=result.name, freq=None)
            if result.freq is None:
                result.freq = to_offset(result.inferred_freq)
            return result

        # to make our life easier, "sort" the two ranges
        if self[0] <= other[0]:
            left, right = self, other
        else:
            left, right = other, self

        # after sorting, the intersection always starts with the right index
        # and ends with the index of which the last elements is smallest
        end = min(left[-1], right[-1])
        start = right[0]

        if end < start:
            return type(self)(data=[])
        else:
            lslice = slice(*left.slice_locs(start, end))
            left_chunk = left.values[lslice]
            return self._shallow_copy(left_chunk)
