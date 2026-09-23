    @property
    def item_dtypes(self):
        result = np.empty(len(self.items), dtype='O')
        mask = np.zeros(len(self.items), dtype=bool)
        for i, blk in enumerate(self.blocks):
            indexer = self.items.get_indexer(blk.items)
            result.put(indexer, blk.dtype.name)
            mask.put(indexer, 1)
        if not (mask.all()):
            raise AssertionError('Some items were not in any block')
        return result
