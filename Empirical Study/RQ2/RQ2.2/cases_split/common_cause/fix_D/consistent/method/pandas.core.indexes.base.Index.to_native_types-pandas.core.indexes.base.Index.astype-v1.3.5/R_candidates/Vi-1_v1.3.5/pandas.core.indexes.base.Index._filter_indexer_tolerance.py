    @final
    def _filter_indexer_tolerance(
        self,
        target: Index | np.ndarray | ExtensionArray,
        indexer: np.ndarray,
        tolerance,
    ) -> np.ndarray:
        own_values = self._get_engine_target()
        distance = abs(own_values[indexer] - target)
        return np.where(distance <= tolerance, indexer, -1)
