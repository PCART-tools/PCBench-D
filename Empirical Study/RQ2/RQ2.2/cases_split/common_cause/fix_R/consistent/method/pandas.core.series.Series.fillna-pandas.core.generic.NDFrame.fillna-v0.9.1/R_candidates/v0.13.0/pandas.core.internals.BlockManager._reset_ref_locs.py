    def _reset_ref_locs(self):
        """ take the current _ref_locs and reset ref_locs on the blocks
            to correctly map, ignoring Nones;
            reset both _items_map and _ref_locs """

        # let's reset the ref_locs in individual blocks
        if self.items.is_unique:
            for b in self.blocks:
                b._ref_locs = None
        else:
            for b in self.blocks:
                b.reset_ref_locs()
        self._rebuild_ref_locs()

        self._ref_locs = None
        self._items_map = None
