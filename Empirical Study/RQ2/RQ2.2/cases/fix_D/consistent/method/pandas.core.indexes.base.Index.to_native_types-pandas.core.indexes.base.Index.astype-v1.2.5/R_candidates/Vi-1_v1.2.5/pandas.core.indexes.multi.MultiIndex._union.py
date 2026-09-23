    def _union(self, other, sort):
        other, result_names = self._convert_can_do_setop(other)

        # TODO: Index.union returns other when `len(self)` is 0.

        if not is_object_dtype(other.dtype):
            raise NotImplementedError(
                "Can only union MultiIndex with MultiIndex or Index of tuples, "
                "try mi.to_flat_index().union(other) instead."
            )

        uniq_tuples = lib.fast_unique_multiple([self._values, other._values], sort=sort)

        return MultiIndex.from_arrays(
            zip(*uniq_tuples), sortorder=0, names=result_names
        )
