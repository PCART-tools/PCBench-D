    @final
    def reindex_axis(
        self,
        new_index: Index,
        axis: AxisInt,
        fill_value=None,
        only_slice: bool = False,
    ) -> Self:
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
            only_slice=only_slice,
        )
