    def _intersection(self, other: Index, sort=False):
        """
        intersection specialized to the case with matching dtypes.
        """
        if self.is_monotonic and other.is_monotonic and self._can_use_libjoin:
            try:
                result = self._inner_indexer(other)[0]
            except TypeError:
                # non-comparable; should only be for object dtype
                pass
            else:
                # TODO: algos.unique1d should preserve DTA/TDA
                res = algos.unique1d(result)
                return ensure_wrapped_if_datetimelike(res)

        res_values = self._intersection_via_get_indexer(other, sort=sort)
        res_values = _maybe_try_sort(res_values, sort)
        return res_values
