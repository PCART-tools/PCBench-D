    def reindex(self, new_axis, indexer=None, method=None, fill_value=None,
                limit=None, copy=True):
        # if we are the same and don't copy, just return
        if not copy and self.index.equals(new_axis):
            return self

        block = self._block.reindex_items_from(new_axis, indexer=indexer,
                                               method=method,
                                               fill_value=fill_value,
                                               limit=limit, copy=copy)
        mgr = SingleBlockManager(block, new_axis)
        mgr._consolidate_inplace()
        return mgr
