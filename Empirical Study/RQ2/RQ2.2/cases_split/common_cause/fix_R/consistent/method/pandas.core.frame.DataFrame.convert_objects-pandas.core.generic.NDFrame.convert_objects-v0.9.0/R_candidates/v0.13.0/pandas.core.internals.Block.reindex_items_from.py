    def reindex_items_from(self, new_ref_items, indexer=None, method=None,
                           fill_value=None, limit=None, copy=True):
        """
        Reindex to only those items contained in the input set of items

        E.g. if you have ['a', 'b'], and the input items is ['b', 'c', 'd'],
        then the resulting items will be ['b']

        Returns
        -------
        reindexed : Block
        """
        if indexer is None:
            new_ref_items, indexer = self.items.reindex(new_ref_items,
                                                        limit=limit)

        needs_fill = method is not None and limit is None
        if fill_value is None:
            fill_value = self.fill_value

        new_items = new_ref_items
        if indexer is None:
            new_values = self.values.copy() if copy else self.values

        else:

            # single block reindex
            if self.ndim == 1:
                new_values = com.take_1d(self.values, indexer,
                                         fill_value=fill_value)
            else:

                masked_idx = indexer[indexer != -1]
                new_items = self.items.take(masked_idx)
                new_values = com.take_nd(self.values, masked_idx, axis=0,
                                         allow_fill=False)
        # fill if needed
        if needs_fill:
            new_values = com.interpolate_2d(new_values, method=method,
                                            limit=limit, fill_value=fill_value)

        block = make_block(new_values, new_items, new_ref_items,
                           ndim=self.ndim, fastpath=True)

        # down cast if needed
        if not self.is_float and (needs_fill or notnull(fill_value)):
            block = block.downcast()

        return block
