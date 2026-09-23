    @final
    def get_indexer_for(self, target, **kwargs) -> np.ndarray:
        """
        Guaranteed return of an indexer even when non-unique.

        This dispatches to get_indexer or get_indexer_non_unique
        as appropriate.

        Returns
        -------
        np.ndarray[np.intp]
            List of indices.
        """
        if self._index_as_unique:
            return self.get_indexer(target, **kwargs)
        indexer, _ = self.get_indexer_non_unique(target)
        return indexer
