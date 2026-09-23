    def _reindex_indexer_items(self, new_items, indexer, fill_value):
        # TODO: less efficient than I'd like

        item_order = com.take_1d(self.items.values, indexer)
        new_axes = [new_items] + self.axes[1:]
        new_blocks = []
        is_unique = new_items.is_unique

        # keep track of what items aren't found anywhere
        l = np.arange(len(item_order))
        mask = np.zeros(len(item_order), dtype=bool)
        for blk in self.blocks:
            blk_indexer = blk.items.get_indexer(item_order)
            selector = blk_indexer != -1

            # update with observed items
            mask |= selector

            if not selector.any():
                continue

            new_block_items = new_items.take(selector.nonzero()[0])
            new_values = com.take_nd(blk.values, blk_indexer[selector], axis=0,
                                     allow_fill=False)
            placement = l[selector] if not is_unique else None
            new_blocks.append(make_block(new_values,
                                         new_block_items,
                                         new_items,
                                         placement=placement,
                                         fastpath=True))

        if not mask.all():
            na_items = new_items[-mask]
            placement = l[-mask] if not is_unique else None
            na_block = self._make_na_block(na_items,
                                           new_items,
                                           placement=placement,
                                           fill_value=fill_value)
            new_blocks.append(na_block)
            new_blocks = _consolidate(new_blocks, new_items)

        return self.__class__(new_blocks, new_axes)
