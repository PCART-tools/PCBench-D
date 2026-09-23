    @final
    def _join_non_unique(
        self, other: Index, how: str_t = "left"
    ) -> tuple[Index, np.ndarray, np.ndarray]:
        # returned ndarrays are np.intp
        from pandas.core.reshape.merge import get_join_indexers

        # We only get here if dtypes match
        assert self.dtype == other.dtype

        lvalues = self._get_join_target()
        rvalues = other._get_join_target()

        left_idx, right_idx = get_join_indexers(
            [lvalues], [rvalues], how=how, sort=True
        )

        left_idx = ensure_platform_int(left_idx)
        right_idx = ensure_platform_int(right_idx)

        join_array = np.asarray(lvalues.take(left_idx))
        mask = left_idx == -1
        np.putmask(join_array, mask, rvalues.take(right_idx))

        join_arraylike = self._from_join_target(join_array)
        join_index = self._wrap_joined_index(join_arraylike, other)

        return join_index, left_idx, right_idx
