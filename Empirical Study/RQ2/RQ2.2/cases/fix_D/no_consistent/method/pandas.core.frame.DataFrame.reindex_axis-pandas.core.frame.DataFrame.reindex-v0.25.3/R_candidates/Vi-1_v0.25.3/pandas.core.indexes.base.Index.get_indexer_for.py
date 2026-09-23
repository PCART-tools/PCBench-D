    def get_indexer_for(self, target, **kwargs):
        """
        Guaranteed return of an indexer even when non-unique.

        This dispatches to get_indexer or get_indexer_nonunique
        as appropriate.

        Returns
        -------
        numpy.ndarray
            List of indices.
        """
        if self.is_unique:
            return self.get_indexer(target, **kwargs)
        indexer, _ = self.get_indexer_non_unique(target, **kwargs)
        return indexer
