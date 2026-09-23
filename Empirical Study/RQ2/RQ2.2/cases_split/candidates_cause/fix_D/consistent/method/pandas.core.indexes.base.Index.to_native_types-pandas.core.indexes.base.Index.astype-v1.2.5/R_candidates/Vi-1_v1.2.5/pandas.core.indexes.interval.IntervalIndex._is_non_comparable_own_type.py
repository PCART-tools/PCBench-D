    def _is_non_comparable_own_type(self, other: "IntervalIndex") -> bool:
        # different closed or incompatible subtype -> no matches

        # TODO: once closed is part of IntervalDtype, we can just define
        #  is_comparable_dtype GH#19371
        if self.closed != other.closed:
            return True
        return not self._is_comparable_dtype(other.dtype)
