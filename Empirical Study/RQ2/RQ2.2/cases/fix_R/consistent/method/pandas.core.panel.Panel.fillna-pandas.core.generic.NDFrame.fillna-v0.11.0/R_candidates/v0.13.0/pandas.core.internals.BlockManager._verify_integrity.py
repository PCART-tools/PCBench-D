    def _verify_integrity(self):
        mgr_shape = self.shape
        tot_items = sum(len(x.items) for x in self.blocks)
        for block in self.blocks:
            if block.ref_items is not self.items:
                raise AssertionError("Block ref_items must be BlockManager "
                                     "items")
            if not block.is_sparse and block.values.shape[1:] != mgr_shape[1:]:
                construction_error(
                    tot_items, block.values.shape[1:], self.axes)
        if len(self.items) != tot_items:
            raise AssertionError('Number of manager items must equal union of '
                                 'block items\n# manager items: {0}, # '
                                 'tot_items: {1}'.format(len(self.items),
                                                         tot_items))
