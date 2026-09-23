    @final
    def _get_nearest_indexer(self, target: "Index", limit, tolerance) -> np.ndarray:
        """
        Get the indexer for the nearest index labels; requires an index with
        values that can be subtracted from each other (e.g., not strings or
        tuples).
        """
        if not len(self):
            return self._get_fill_indexer(target, "pad")

        left_indexer = self.get_indexer(target, "pad", limit=limit)
        right_indexer = self.get_indexer(target, "backfill", limit=limit)

        target_values = target._values
        # error: Unsupported left operand type for - ("ExtensionArray")
        left_distances = np.abs(
            self._values[left_indexer] - target_values  # type: ignore[operator]
        )
        # error: Unsupported left operand type for - ("ExtensionArray")
        right_distances = np.abs(
            self._values[right_indexer] - target_values  # type: ignore[operator]
        )

        op = operator.lt if self.is_monotonic_increasing else operator.le
        indexer = np.where(
            op(left_distances, right_distances) | (right_indexer == -1),
            left_indexer,
            right_indexer,
        )
        if tolerance is not None:
            indexer = self._filter_indexer_tolerance(target_values, indexer, tolerance)
        return indexer
