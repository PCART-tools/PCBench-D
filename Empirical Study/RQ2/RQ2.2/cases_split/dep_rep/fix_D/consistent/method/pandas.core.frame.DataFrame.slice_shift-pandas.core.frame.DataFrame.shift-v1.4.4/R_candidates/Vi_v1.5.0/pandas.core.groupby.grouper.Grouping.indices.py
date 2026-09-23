    @cache_readonly
    def indices(self) -> dict[Hashable, npt.NDArray[np.intp]]:
        # we have a list of groupers
        if isinstance(self.grouping_vector, ops.BaseGrouper):
            return self.grouping_vector.indices

        values = Categorical(self.grouping_vector)
        return values._reverse_indexer()
