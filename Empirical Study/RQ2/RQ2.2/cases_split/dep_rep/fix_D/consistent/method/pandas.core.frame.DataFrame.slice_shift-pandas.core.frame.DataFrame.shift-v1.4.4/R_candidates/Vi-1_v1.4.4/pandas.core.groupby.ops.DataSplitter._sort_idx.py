    @cache_readonly
    def _sort_idx(self) -> npt.NDArray[np.intp]:
        # Counting sort indexer
        return get_group_index_sorter(self.labels, self.ngroups)
