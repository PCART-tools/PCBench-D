    def _cython_agg_general(
        self, how: str, alt=None, numeric_only: bool = True, min_count: int = -1
    ) -> DataFrame:
        agg_blocks, agg_items = self._cython_agg_blocks(
            how, alt=alt, numeric_only=numeric_only, min_count=min_count
        )
        return self._wrap_agged_blocks(agg_blocks, items=agg_items)
