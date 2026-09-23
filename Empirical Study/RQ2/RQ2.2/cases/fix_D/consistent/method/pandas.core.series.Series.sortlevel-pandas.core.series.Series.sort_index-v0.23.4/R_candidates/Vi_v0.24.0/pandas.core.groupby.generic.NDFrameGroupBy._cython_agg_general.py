    def _cython_agg_general(self, how, alt=None, numeric_only=True,
                            min_count=-1):
        new_items, new_blocks = self._cython_agg_blocks(
            how, alt=alt, numeric_only=numeric_only, min_count=min_count)
        return self._wrap_agged_blocks(new_items, new_blocks)
