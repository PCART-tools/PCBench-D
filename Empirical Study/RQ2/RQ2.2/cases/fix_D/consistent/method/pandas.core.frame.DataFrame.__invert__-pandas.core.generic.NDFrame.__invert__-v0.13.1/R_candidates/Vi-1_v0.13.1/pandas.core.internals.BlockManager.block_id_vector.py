    @property
    def block_id_vector(self):
        # TODO
        result = np.empty(len(self.items), dtype=int)
        result.fill(-1)

        for i, blk in enumerate(self.blocks):
            indexer = self.items.get_indexer(blk.items)
            if (indexer == -1).any():
                raise AssertionError('Block items must be in manager items')
            result.put(indexer, i)

        if (result < 0).any():
            raise AssertionError('Some items were not in any block')
        return result
