    def take(
        self,
        indexer: npt.NDArray[np.intp],
        axis: AxisInt = 1,
        verify: bool = True,
    ) -> Self:
        """
        Take items along any axis.
        """
        assert isinstance(indexer, np.ndarray), type(indexer)
        assert indexer.dtype == np.intp, indexer.dtype

        axis = self._normalize_axis(axis)

        if not indexer.ndim == 1:
            raise ValueError("indexer should be 1-dimensional")

        n = self.shape_proper[axis]
        indexer = maybe_convert_indices(indexer, n, verify=verify)

        new_labels = self._axes[axis].take(indexer)
        return self._reindex_indexer(
            new_axis=new_labels, indexer=indexer, axis=axis, allow_dups=True
        )
