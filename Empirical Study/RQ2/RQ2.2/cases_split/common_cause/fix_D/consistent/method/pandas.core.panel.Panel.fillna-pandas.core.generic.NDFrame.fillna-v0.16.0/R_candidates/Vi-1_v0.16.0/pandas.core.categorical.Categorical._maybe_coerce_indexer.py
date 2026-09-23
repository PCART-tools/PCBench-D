    def _maybe_coerce_indexer(self, indexer):
        """ return an indexer coerced to the codes dtype """
        if isinstance(indexer, np.ndarray) and indexer.dtype.kind == 'i':
            indexer = indexer.astype(self._codes.dtype)
        return indexer
