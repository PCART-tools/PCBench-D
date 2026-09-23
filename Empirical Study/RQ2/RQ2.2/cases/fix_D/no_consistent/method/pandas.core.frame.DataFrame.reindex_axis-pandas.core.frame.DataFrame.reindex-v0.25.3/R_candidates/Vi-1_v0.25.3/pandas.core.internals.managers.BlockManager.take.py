    def take(self, indexer, axis=1, verify=True, convert=True):
        """
        Take items along any axis.
        """
        self._consolidate_inplace()
        indexer = (
            np.arange(indexer.start, indexer.stop, indexer.step, dtype="int64")
            if isinstance(indexer, slice)
            else np.asanyarray(indexer, dtype="int64")
        )

        n = self.shape[axis]
        if convert:
            indexer = maybe_convert_indices(indexer, n)

        if verify:
            if ((indexer == -1) | (indexer >= n)).any():
                raise Exception("Indices must be nonzero and less than the axis length")

        new_labels = self.axes[axis].take(indexer)
        return self.reindex_indexer(
            new_axis=new_labels, indexer=indexer, axis=axis, allow_dups=True
        )
