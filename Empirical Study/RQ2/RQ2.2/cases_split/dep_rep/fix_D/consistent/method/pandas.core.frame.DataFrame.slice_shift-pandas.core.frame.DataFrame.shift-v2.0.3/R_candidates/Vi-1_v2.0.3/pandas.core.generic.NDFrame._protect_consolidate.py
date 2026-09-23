    @final
    def _protect_consolidate(self, f):
        """
        Consolidate _mgr -- if the blocks have changed, then clear the
        cache
        """
        if isinstance(self._mgr, (ArrayManager, SingleArrayManager)):
            return f()
        blocks_before = len(self._mgr.blocks)
        result = f()
        if len(self._mgr.blocks) != blocks_before:
            self._clear_item_cache()
        return result
