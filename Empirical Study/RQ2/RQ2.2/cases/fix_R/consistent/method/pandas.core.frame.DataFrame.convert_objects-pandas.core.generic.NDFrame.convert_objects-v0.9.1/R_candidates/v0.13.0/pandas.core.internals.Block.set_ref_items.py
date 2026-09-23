    def set_ref_items(self, ref_items, maybe_rename=True):
        """
        If maybe_rename=True, need to set the items for this guy
        """
        if not isinstance(ref_items, Index):
            raise AssertionError('block ref_items must be an Index')
        if maybe_rename == 'clear':
            self._ref_locs = None
        elif maybe_rename:
            self.items = ref_items.take(self.ref_locs)
        self.ref_items = ref_items
