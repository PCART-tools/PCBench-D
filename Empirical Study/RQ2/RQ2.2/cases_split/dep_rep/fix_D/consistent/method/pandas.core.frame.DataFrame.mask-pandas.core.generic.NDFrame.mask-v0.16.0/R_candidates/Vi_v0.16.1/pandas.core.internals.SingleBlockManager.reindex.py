    def reindex(self, new_axis, indexer=None, method=None, fill_value=None,
                limit=None, copy=True):
        # if we are the same and don't copy, just return
        if self.index.equals(new_axis):
            if copy:
                return self.copy(deep=True)
            else:
                return self

        values = self._block.get_values()

        if indexer is None:
            indexer = self.items.get_indexer_for(new_axis)

        if fill_value is None:
            # FIXME: is fill_value used correctly in sparse blocks?
            if not self._block.is_sparse:
                fill_value = self._block.fill_value
            else:
                fill_value = np.nan

        new_values = com.take_1d(values, indexer,
                                 fill_value=fill_value)

        # fill if needed
        if method is not None or limit is not None:
            new_values = com.interpolate_2d(new_values, method=method,
                                            limit=limit, fill_value=fill_value)

        if self._block.is_sparse:
            make_block = self._block.make_block_same_class

        block = make_block(new_values, copy=copy,
                           placement=slice(0, len(new_axis)))

        mgr = SingleBlockManager(block, new_axis)
        mgr._consolidate_inplace()
        return mgr
