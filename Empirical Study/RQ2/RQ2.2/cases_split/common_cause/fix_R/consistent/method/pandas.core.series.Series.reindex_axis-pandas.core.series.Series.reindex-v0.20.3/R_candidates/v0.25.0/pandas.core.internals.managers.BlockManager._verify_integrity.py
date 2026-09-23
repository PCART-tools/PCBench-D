    def _verify_integrity(self):
        mgr_shape = self.shape
        tot_items = sum(len(x.mgr_locs) for x in self.blocks)
        for block in self.blocks:
            if block._verify_integrity and block.shape[1:] != mgr_shape[1:]:
                construction_error(tot_items, block.shape[1:], self.axes)
        if len(self.items) != tot_items:
            raise AssertionError(
                "Number of manager items must equal union of "
                "block items\n# manager items: {0}, # "
                "tot_items: {1}".format(len(self.items), tot_items)
            )
