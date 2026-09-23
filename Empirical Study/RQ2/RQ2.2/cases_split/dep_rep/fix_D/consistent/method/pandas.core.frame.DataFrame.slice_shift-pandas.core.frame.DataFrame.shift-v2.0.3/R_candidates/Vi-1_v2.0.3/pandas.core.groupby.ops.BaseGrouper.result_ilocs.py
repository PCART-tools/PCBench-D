    @final
    def result_ilocs(self) -> npt.NDArray[np.intp]:
        """
        Get the original integer locations of result_index in the input.
        """
        # Original indices are where group_index would go via sorting.
        # But when dropna is true, we need to remove null values while accounting for
        # any gaps that then occur because of them.
        group_index = get_group_index(
            self.codes, self.shape, sort=self._sort, xnull=True
        )
        group_index, _ = compress_group_index(group_index, sort=self._sort)

        if self.has_dropped_na:
            mask = np.where(group_index >= 0)
            # Count how many gaps are caused by previous null values for each position
            null_gaps = np.cumsum(group_index == -1)[mask]
            group_index = group_index[mask]

        result = get_group_index_sorter(group_index, self.ngroups)

        if self.has_dropped_na:
            # Shift by the number of prior null gaps
            result += np.take(null_gaps, result)

        return result
