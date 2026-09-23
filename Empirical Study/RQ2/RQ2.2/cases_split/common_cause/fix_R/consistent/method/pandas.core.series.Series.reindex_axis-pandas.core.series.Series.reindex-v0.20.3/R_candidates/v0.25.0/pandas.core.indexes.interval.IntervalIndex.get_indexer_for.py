    def get_indexer_for(self, target: AnyArrayLike, **kwargs) -> np.ndarray:
        """
        Guaranteed return of an indexer even when overlapping.

        This dispatches to get_indexer or get_indexer_non_unique
        as appropriate.

        Returns
        -------
        numpy.ndarray
            List of indices.
        """
        if self.is_overlapping:
            return self.get_indexer_non_unique(target, **kwargs)[0]
        return self.get_indexer(target, **kwargs)
