    @cache_readonly
    def slabels(self) -> npt.NDArray[np.intp]:
        # Sorted labels
        return self.labels.take(self._sort_idx)
