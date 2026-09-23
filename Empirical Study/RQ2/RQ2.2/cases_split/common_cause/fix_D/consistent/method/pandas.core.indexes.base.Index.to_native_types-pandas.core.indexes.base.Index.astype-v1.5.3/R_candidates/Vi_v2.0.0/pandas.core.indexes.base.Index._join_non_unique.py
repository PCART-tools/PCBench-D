    @final
    def _join_non_unique(
        self, other: Index, how: JoinHow = "left"
    ) -> tuple[Index, npt.NDArray[np.intp], npt.NDArray[np.intp]]:
        from pandas.core.reshape.merge import get_join_indexers

        # We only get here if dtypes match
        assert self.dtype == other.dtype

        left_idx, right_idx = get_join_indexers(
            [self._values], [other._values], how=how, sort=True
        )
        mask = left_idx == -1

        join_idx = self.take(left_idx)
        right = other.take(right_idx)
        join_index = join_idx.putmask(mask, right)
        return join_index, left_idx, right_idx
