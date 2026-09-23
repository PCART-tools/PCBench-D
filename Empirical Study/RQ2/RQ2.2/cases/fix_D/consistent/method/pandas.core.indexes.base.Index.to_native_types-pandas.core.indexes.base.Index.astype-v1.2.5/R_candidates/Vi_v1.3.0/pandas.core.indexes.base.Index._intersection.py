    def _intersection(self, other: Index, sort=False):
        """
        intersection specialized to the case with matching dtypes.
        """
        if (
            self.is_monotonic
            and other.is_monotonic
            and not is_interval_dtype(self.dtype)
        ):
            # For IntervalIndex _inner_indexer is not more performant than get_indexer,
            #  so don't take this fastpath
            try:
                result = self._inner_indexer(other)[0]
            except TypeError:
                pass
            else:
                # TODO: algos.unique1d should preserve DTA/TDA
                res = algos.unique1d(result)
                return ensure_wrapped_if_datetimelike(res)

        res_values = self._intersection_via_get_indexer(other, sort=sort)
        res_values = _maybe_try_sort(res_values, sort)
        return res_values
