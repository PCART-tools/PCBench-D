    def reindex_items(self, new_items, indexer=None, copy=True,
                      fill_value=None):
        """

        """
        new_items = _ensure_index(new_items)
        data = self
        if not data.is_consolidated():
            data = data.consolidate()
            return data.reindex_items(new_items, copy=copy,
                                      fill_value=fill_value)

        if indexer is None:
            new_items, indexer = self.items.reindex(new_items,
                                                    copy_if_needed=True)
        new_axes = [new_items] + self.axes[1:]

        # could have so me pathological (MultiIndex) issues here
        new_blocks = []
        if indexer is None:
            for blk in self.blocks:
                if copy:
                    blk = blk.reindex_items_from(new_items)
                else:
                    blk.ref_items = new_items
                new_blocks.extend(_valid_blocks(blk))
        else:

            # unique
            if self.axes[0].is_unique and new_items.is_unique:

                for block in self.blocks:
                    blk = block.reindex_items_from(new_items, copy=copy)
                    new_blocks.extend(_valid_blocks(blk))

            # non-unique
            else:
                rl = self._set_ref_locs(do_refs='force')
                for i, idx in enumerate(indexer):
                    blk, lidx = rl[idx]
                    item = new_items.take([i])
                    blk = make_block(_block_shape(blk.iget(lidx)), item,
                                     new_items, ndim=self.ndim, fastpath=True,
                                     placement=[i])
                    new_blocks.append(blk)

            # add a na block if we are missing items
            mask = indexer == -1
            if mask.any():
                extra_items = new_items[mask]
                na_block = self._make_na_block(extra_items, new_items,
                                               fill_value=fill_value)
                new_blocks.append(na_block)
                new_blocks = _consolidate(new_blocks, new_items)

        return self.__class__(new_blocks, new_axes)
