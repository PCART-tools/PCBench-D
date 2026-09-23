    def _intersection(self, other: Index, sort=False) -> Index:
        """
        intersection specialized to the case with matching dtypes.
        """
        if len(self) == 0:
            return self.copy()._get_reconciled_name_object(other)
        if len(other) == 0:
            return other.copy()._get_reconciled_name_object(self)

        if not isinstance(other, type(self)):
            result = Index.intersection(self, other, sort=sort)
            return result

        elif not self._can_fast_intersect(other):
            result = Index._intersection(self, other, sort=sort)
            # We need to invalidate the freq because Index._intersection
            #  uses _shallow_copy on a view of self._data, which will preserve
            #  self.freq if we're not careful.
            result = self._wrap_setop_result(other, result)
            return result._with_freq(None)._with_freq("infer")

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
            result = self[:0]
        else:
            lslice = slice(*left.slice_locs(start, end))
            left_chunk = left._values[lslice]
            # error: Argument 1 to "_simple_new" of "DatetimeIndexOpsMixin" has
            # incompatible type "Union[ExtensionArray, Any]"; expected
            # "Union[DatetimeArray, TimedeltaArray, PeriodArray]"  [arg-type]
            result = type(self)._simple_new(left_chunk)  # type: ignore[arg-type]

        return self._wrap_setop_result(other, result)
