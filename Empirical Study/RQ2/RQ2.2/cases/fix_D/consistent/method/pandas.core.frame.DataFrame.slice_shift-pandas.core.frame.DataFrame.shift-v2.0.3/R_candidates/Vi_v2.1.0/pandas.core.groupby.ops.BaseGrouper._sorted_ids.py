    @final
    @cache_readonly
    def _sorted_ids(self) -> npt.NDArray[np.intp]:
        ids, _, _ = self.group_info
        return ids.take(self._sort_idx)
