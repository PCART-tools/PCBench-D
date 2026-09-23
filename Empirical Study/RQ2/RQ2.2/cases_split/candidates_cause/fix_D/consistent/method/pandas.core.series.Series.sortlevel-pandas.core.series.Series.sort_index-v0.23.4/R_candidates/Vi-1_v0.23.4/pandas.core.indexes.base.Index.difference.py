    def difference(self, other):
        """
        Return a new Index with elements from the index that are not in
        `other`.

        This is the set difference of two Index objects.
        It's sorted if sorting is possible.

        Parameters
        ----------
        other : Index or array-like

        Returns
        -------
        difference : Index

        Examples
        --------

        >>> idx1 = pd.Index([1, 2, 3, 4])
        >>> idx2 = pd.Index([3, 4, 5, 6])
        >>> idx1.difference(idx2)
        Int64Index([1, 2], dtype='int64')

        """
        self._assert_can_do_setop(other)

        if self.equals(other):
            return self._shallow_copy([])

        other, result_name = self._convert_can_do_setop(other)

        this = self._get_unique_index()

        indexer = this.get_indexer(other)
        indexer = indexer.take((indexer != -1).nonzero()[0])

        label_diff = np.setdiff1d(np.arange(this.size), indexer,
                                  assume_unique=True)
        the_diff = this.values.take(label_diff)
        try:
            the_diff = sorting.safe_sort(the_diff)
        except TypeError:
            pass

        return this._shallow_copy(the_diff, name=result_name, freq=None)
