    def take(
        self: T,
        indexer,
        axis: int = 1,
        verify: bool = True,
        convert_indices: bool = True,
    ) -> T:
        """
        Take items along any axis.
        """
        axis = self._normalize_axis(axis)

        indexer = (
            np.arange(indexer.start, indexer.stop, indexer.step, dtype="int64")
            if isinstance(indexer, slice)
            else np.asanyarray(indexer, dtype="int64")
        )

        if not indexer.ndim == 1:
            raise ValueError("indexer should be 1-dimensional")

        n = self.shape_proper[axis]
        if convert_indices:
            indexer = maybe_convert_indices(indexer, n, verify=verify)

        new_labels = self._axes[axis].take(indexer)
        return self._reindex_indexer(
            new_axis=new_labels, indexer=indexer, axis=axis, allow_dups=True
        )
