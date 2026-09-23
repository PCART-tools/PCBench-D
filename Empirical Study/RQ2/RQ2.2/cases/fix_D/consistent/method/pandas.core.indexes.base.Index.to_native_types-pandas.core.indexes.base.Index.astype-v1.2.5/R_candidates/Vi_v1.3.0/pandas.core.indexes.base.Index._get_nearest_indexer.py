    @final
    def _get_nearest_indexer(
        self, target: Index, limit: int | None, tolerance
    ) -> np.ndarray:
        """
        Get the indexer for the nearest index labels; requires an index with
        values that can be subtracted from each other (e.g., not strings or
        tuples).
        """
        if not len(self):
            return self._get_fill_indexer(target, "pad")

        left_indexer = self.get_indexer(target, "pad", limit=limit)
        right_indexer = self.get_indexer(target, "backfill", limit=limit)

        target_values = target._get_engine_target()
        own_values = self._get_engine_target()
        left_distances = np.abs(own_values[left_indexer] - target_values)
        right_distances = np.abs(own_values[right_indexer] - target_values)

        op = operator.lt if self.is_monotonic_increasing else operator.le
        indexer = np.where(
            op(left_distances, right_distances) | (right_indexer == -1),
            left_indexer,
            right_indexer,
        )
        if tolerance is not None:
            indexer = self._filter_indexer_tolerance(target_values, indexer, tolerance)
        return indexer
