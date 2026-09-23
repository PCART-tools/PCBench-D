    @final
    def _get_fill_indexer(
        self, target: "Index", method: str_t, limit=None, tolerance=None
    ) -> np.ndarray:

        target_values = target._get_engine_target()

        if self.is_monotonic_increasing and target.is_monotonic_increasing:
            engine_method = (
                self._engine.get_pad_indexer
                if method == "pad"
                else self._engine.get_backfill_indexer
            )
            indexer = engine_method(target_values, limit)
        else:
            indexer = self._get_fill_indexer_searchsorted(target, method, limit)
        if tolerance is not None and len(self):
            indexer = self._filter_indexer_tolerance(target_values, indexer, tolerance)
        return indexer
