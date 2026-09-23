    def _consolidate_inplace(self):
        if not self.is_consolidated():
            self.blocks = _consolidate(self.blocks, self.items)

            # reset our mappings
            if not self.items.is_unique:
                self._ref_locs = None
                self._items_map = None
                self._set_ref_locs(do_refs=True)

            self._is_consolidated = True
            self._known_consolidated = True
            self._set_has_sparse()
