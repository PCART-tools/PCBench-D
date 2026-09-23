    def _consolidate_inplace(self) -> None:
        # In general, _consolidate_inplace should only be called via
        #  DataFrame._consolidate_inplace, otherwise we will fail to invalidate
        #  the DataFrame's _item_cache. The exception is for newly-created
        #  BlockManager objects not yet attached to a DataFrame.
        if not self.is_consolidated():
            if self.refs is None:
                self.blocks = _consolidate(self.blocks)
            else:
                self.blocks, self.refs = _consolidate_with_refs(self.blocks, self.refs)
            self._is_consolidated = True
            self._known_consolidated = True
            self._rebuild_blknos_and_blklocs()
