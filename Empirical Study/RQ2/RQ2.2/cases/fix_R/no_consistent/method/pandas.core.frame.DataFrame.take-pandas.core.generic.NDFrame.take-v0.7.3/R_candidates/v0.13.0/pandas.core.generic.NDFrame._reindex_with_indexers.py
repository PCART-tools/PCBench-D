    def _reindex_with_indexers(self, reindexers, method=None,
                               fill_value=np.nan, limit=None, copy=False,
                               allow_dups=False):
        """ allow_dups indicates an internal call here """

        # reindex doing multiple operations on different axes if indiciated
        new_data = self._data
        for axis in sorted(reindexers.keys()):
            index, indexer = reindexers[axis]
            baxis = self._get_block_manager_axis(axis)

            if index is None:
                continue
            index = _ensure_index(index)

            # reindex the axis
            if method is not None:
                new_data = new_data.reindex_axis(
                    index, indexer=indexer, method=method, axis=baxis,
                    fill_value=fill_value, limit=limit, copy=copy)

            elif indexer is not None:
                # TODO: speed up on homogeneous DataFrame objects
                indexer = com._ensure_int64(indexer)
                new_data = new_data.reindex_indexer(index, indexer, axis=baxis,
                                                    fill_value=fill_value,
                                                    allow_dups=allow_dups)

            elif (baxis == 0 and index is not None and
                    index is not new_data.axes[baxis]):
                new_data = new_data.reindex_items(index, copy=copy,
                                                  fill_value=fill_value)

            elif (baxis > 0 and index is not None and
                    index is not new_data.axes[baxis]):
                new_data = new_data.copy(deep=copy)
                new_data.set_axis(baxis, index)

        if copy and new_data is self._data:
            new_data = new_data.copy()

        return self._constructor(new_data).__finalize__(self)
