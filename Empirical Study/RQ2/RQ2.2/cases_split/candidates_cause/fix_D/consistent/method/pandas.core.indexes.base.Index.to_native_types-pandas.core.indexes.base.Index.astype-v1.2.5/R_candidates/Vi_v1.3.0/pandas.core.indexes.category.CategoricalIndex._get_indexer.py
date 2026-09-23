    def _get_indexer(
        self,
        target: Index,
        method: str | None = None,
        limit: int | None = None,
        tolerance=None,
    ) -> np.ndarray:
        # returned ndarray is np.intp

        if self.equals(target):
            return np.arange(len(self), dtype="intp")

        return self._get_indexer_non_unique(target._values)[0]
