    def intersection(self, other):
        """
        Form the intersection of two Index objects.

        This returns a new Index with elements common to the index and `other`,
        preserving the order of the calling index.

        Parameters
        ----------
        other : Index or array-like

        Returns
        -------
        intersection : Index

        Examples
        --------

        >>> idx1 = pd.Index([1, 2, 3, 4])
        >>> idx2 = pd.Index([3, 4, 5, 6])
        >>> idx1.intersection(idx2)
        Int64Index([3, 4], dtype='int64')

        """
        self._assert_can_do_setop(other)
        other = _ensure_index(other)

        if self.equals(other):
            return self._get_consensus_name(other)

        if not is_dtype_equal(self.dtype, other.dtype):
            this = self.astype('O')
            other = other.astype('O')
            return this.intersection(other)

        # TODO(EA): setops-refactor, clean all this up
        if is_period_dtype(self):
            lvals = self._ndarray_values
        else:
            lvals = self._values
        if is_period_dtype(other):
            rvals = other._ndarray_values
        else:
            rvals = other._values

        if self.is_monotonic and other.is_monotonic:
            try:
                result = self._inner_indexer(lvals, rvals)[0]
                return self._wrap_union_result(other, result)
            except TypeError:
                pass

        try:
            indexer = Index(rvals).get_indexer(lvals)
            indexer = indexer.take((indexer != -1).nonzero()[0])
        except Exception:
            # duplicates
            indexer = algos.unique1d(
                Index(rvals).get_indexer_non_unique(lvals)[0])
            indexer = indexer[indexer != -1]

        taken = other.take(indexer)
        if self.name != other.name:
            taken.name = None
        return taken
