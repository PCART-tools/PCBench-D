    def _cython_agg_general(self, how, alt=None, numeric_only=True):
        new_items, new_blocks = self._cython_agg_blocks(
            how, alt=alt, numeric_only=numeric_only)
        return self._wrap_agged_blocks(new_items, new_blocks)
