    def _reindex_with_indexers(self, reindexers, fill_value=None, copy=False,
                               allow_dups=False):
        """allow_dups indicates an internal call here """

        # reindex doing multiple operations on different axes if indicated
        new_data = self._data
        for axis in sorted(reindexers.keys()):
            index, indexer = reindexers[axis]
            baxis = self._get_block_manager_axis(axis)

            if index is None:
                continue

            index = ensure_index(index)
            if indexer is not None:
                indexer = ensure_int64(indexer)

            # TODO: speed up on homogeneous DataFrame objects
            new_data = new_data.reindex_indexer(index, indexer, axis=baxis,
                                                fill_value=fill_value,
                                                allow_dups=allow_dups,
                                                copy=copy)

        if copy and new_data is self._data:
            new_data = new_data.copy()

        return self._constructor(new_data).__finalize__(self)
