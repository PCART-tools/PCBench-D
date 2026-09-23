    @final
    def reindex_axis(
        self: T,
        new_index: Index,
        axis: int,
        fill_value=None,
        consolidate: bool = True,
        only_slice: bool = False,
    ) -> T:
        """
        Conform data manager to new index.
        """
        new_index, indexer = self.axes[axis].reindex(new_index)

        return self.reindex_indexer(
            new_index,
            indexer,
            axis=axis,
            fill_value=fill_value,
            copy=False,
            consolidate=consolidate,
            only_slice=only_slice,
        )
