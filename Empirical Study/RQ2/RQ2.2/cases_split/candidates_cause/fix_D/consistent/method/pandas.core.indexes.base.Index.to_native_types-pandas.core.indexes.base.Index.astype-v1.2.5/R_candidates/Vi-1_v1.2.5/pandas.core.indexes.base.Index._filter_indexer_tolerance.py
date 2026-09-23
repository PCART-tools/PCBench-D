    @final
    def _filter_indexer_tolerance(
        self,
        target: Union["Index", np.ndarray, ExtensionArray],
        indexer: np.ndarray,
        tolerance,
    ) -> np.ndarray:
        # error: Unsupported left operand type for - ("ExtensionArray")
        distance = abs(self._values[indexer] - target)  # type: ignore[operator]
        indexer = np.where(distance <= tolerance, indexer, -1)
        return indexer
