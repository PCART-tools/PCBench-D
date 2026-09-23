    def reindex_indexer(
        self,
        new_axis,
        indexer,
        axis: AxisInt,
        fill_value=None,
        allow_dups: bool = False,
        copy: bool = True,
        only_slice: bool = False,
    ) -> Self:
        raise AbstractMethodError(self)
