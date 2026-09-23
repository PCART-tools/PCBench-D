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

        # 1-d always
        if indexer is None:
            new_ref_items, indexer = self.items.reindex(new_ref_items,
                                                        limit=limit)
        if indexer is None:
            indexer = np.arange(len(self.items))

        # single block
        if self.ndim == 1:

            new_items = new_ref_items
            new_values = com.take_1d(self.values.values, indexer)

        else:

            # if we don't overlap at all, then don't include this block
            new_items = self.items & new_ref_items
            if not len(new_items):
                return None

            new_values = self.values.values

        # fill if needed
        if method is not None or limit is not None:
            if fill_value is None:
                fill_value = self.fill_value
            new_values = com.interpolate_2d(new_values, method=method,
                                            limit=limit, fill_value=fill_value)

        return self.make_block(new_values, items=new_items,
                               ref_items=new_ref_items, copy=copy)
