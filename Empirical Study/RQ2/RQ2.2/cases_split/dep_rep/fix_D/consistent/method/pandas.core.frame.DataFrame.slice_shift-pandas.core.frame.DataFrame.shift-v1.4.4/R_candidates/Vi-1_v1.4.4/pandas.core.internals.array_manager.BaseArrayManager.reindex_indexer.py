    def reindex_indexer(
        self: T,
        new_axis,
        indexer,
        axis: int,
        fill_value=None,
        allow_dups: bool = False,
        copy: bool = True,
        # ignored keywords
        consolidate: bool = True,
        only_slice: bool = False,
        # ArrayManager specific keywords
        use_na_proxy: bool = False,
    ) -> T:
        axis = self._normalize_axis(axis)
        return self._reindex_indexer(
            new_axis,
            indexer,
            axis,
            fill_value,
            allow_dups,
            copy,
            use_na_proxy,
        )
