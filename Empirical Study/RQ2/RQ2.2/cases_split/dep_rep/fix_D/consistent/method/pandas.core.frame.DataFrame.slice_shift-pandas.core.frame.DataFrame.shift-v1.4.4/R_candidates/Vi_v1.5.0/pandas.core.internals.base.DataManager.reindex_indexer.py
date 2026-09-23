    def reindex_indexer(
        self: T,
        new_axis,
        indexer,
        axis: int,
        fill_value=None,
        allow_dups: bool = False,
        copy: bool = True,
        only_slice: bool = False,
    ) -> T:
        raise AbstractMethodError(self)
