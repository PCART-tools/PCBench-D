    @final
    def _reindex_with_indexers(
        self: NDFrameT,
        reindexers,
        fill_value=None,
        copy: bool_t = False,
        allow_dups: bool_t = False,
    ) -> NDFrameT:
        """allow_dups indicates an internal call here"""
        # reindex doing multiple operations on different axes if indicated
        new_data = self._mgr
        for axis in sorted(reindexers.keys()):
            index, indexer = reindexers[axis]
            baxis = self._get_block_manager_axis(axis)

            if index is None:
                continue

            index = ensure_index(index)
            if indexer is not None:
                indexer = ensure_platform_int(indexer)

            # TODO: speed up on homogeneous DataFrame objects (see _reindex_multi)
            new_data = new_data.reindex_indexer(
                index,
                indexer,
                axis=baxis,
                fill_value=fill_value,
                allow_dups=allow_dups,
                copy=copy,
            )
            # If we've made a copy once, no need to make another one
            copy = False

        if copy and new_data is self._mgr:
            new_data = new_data.copy()

        return self._constructor(new_data).__finalize__(self)
