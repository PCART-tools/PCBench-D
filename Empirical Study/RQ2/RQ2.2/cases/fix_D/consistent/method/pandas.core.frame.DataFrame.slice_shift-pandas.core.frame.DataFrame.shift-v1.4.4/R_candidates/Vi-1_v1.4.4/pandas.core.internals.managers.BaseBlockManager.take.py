    def take(self: T, indexer, axis: int = 1, verify: bool = True) -> T:
        """
        Take items along any axis.

        indexer : np.ndarray or slice
        axis : int, default 1
        verify : bool, default True
            Check that all entries are between 0 and len(self) - 1, inclusive.
            Pass verify=False if this check has been done by the caller.

        Returns
        -------
        BlockManager
        """
        # We have 6 tests that get here with a slice
        indexer = (
            np.arange(indexer.start, indexer.stop, indexer.step, dtype=np.intp)
            if isinstance(indexer, slice)
            else np.asanyarray(indexer, dtype=np.intp)
        )

        n = self.shape[axis]
        indexer = maybe_convert_indices(indexer, n, verify=verify)

        new_labels = self.axes[axis].take(indexer)
        return self.reindex_indexer(
            new_axis=new_labels,
            indexer=indexer,
            axis=axis,
            allow_dups=True,
            consolidate=False,
        )
