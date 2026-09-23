    @final
    def _join_non_unique(self, other, how="left", return_indexers=False):
        from pandas.core.reshape.merge import get_join_indexers

        # We only get here if dtypes match
        assert self.dtype == other.dtype

        lvalues = self._get_engine_target()
        rvalues = other._get_engine_target()

        left_idx, right_idx = get_join_indexers(
            [lvalues], [rvalues], how=how, sort=True
        )

        left_idx = ensure_platform_int(left_idx)
        right_idx = ensure_platform_int(right_idx)

        join_index = np.asarray(lvalues.take(left_idx))
        mask = left_idx == -1
        np.putmask(join_index, mask, rvalues.take(right_idx))

        join_index = self._wrap_joined_index(join_index, other)

        if return_indexers:
            return join_index, left_idx, right_idx
        else:
            return join_index
