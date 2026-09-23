    def _protect_consolidate(self, f):
        blocks_before = len(self._data.blocks)
        result = f()
        if len(self._data.blocks) != blocks_before:
            self._clear_item_cache()
        return result
