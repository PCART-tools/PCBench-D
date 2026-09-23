    def split_block_at(self, item):
        if len(self.items) == 1 and item == self.items[0]:
            return []
        return super(SparseBlock, self).split_block_at(self, item)
