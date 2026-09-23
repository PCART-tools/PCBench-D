    def _interleave(self, items):
        """
        Return ndarray from blocks with specified item order
        Items must be contained in the blocks
        """
        dtype = _interleaved_dtype(self.blocks)
        items = _ensure_index(items)

        result = np.empty(self.shape, dtype=dtype)
        itemmask = np.zeros(len(items), dtype=bool)

        # By construction, all of the item should be covered by one of the
        # blocks
        if items.is_unique:

            for block in self.blocks:
                indexer = items.get_indexer(block.items)
                if (indexer == -1).any():
                    raise AssertionError('Items must contain all block items')
                result[indexer] = block.get_values(dtype)
                itemmask[indexer] = 1

        else:

            # non-unique, must use ref_locs
            rl = self._set_ref_locs()
            for i, (block, idx) in enumerate(rl):
                result[i] = block.get_values(dtype)[idx]
                itemmask[i] = 1

        if not itemmask.all():
            raise AssertionError('Some items were not contained in blocks')

        return result
