    @final
    @cache_readonly
    def _sort_idx(self) -> npt.NDArray[np.intp]:
        # Counting sort indexer
        ids, _, ngroups = self.group_info
        return get_group_index_sorter(ids, ngroups)
