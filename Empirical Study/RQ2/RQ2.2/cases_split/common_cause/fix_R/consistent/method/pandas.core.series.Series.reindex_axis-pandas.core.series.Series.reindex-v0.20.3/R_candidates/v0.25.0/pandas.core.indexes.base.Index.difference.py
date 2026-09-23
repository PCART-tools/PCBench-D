    def difference(self, other, sort=None):
        """
        Return a new Index with elements from the index that are not in
        `other`.

        This is the set difference of two Index objects.

        Parameters
        ----------
        other : Index or array-like
        sort : False or None, default None
            Whether to sort the resulting index. By default, the
            values are attempted to be sorted, but any TypeError from
            incomparable elements is caught by pandas.

            * None : Attempt to sort the result, but catch any TypeErrors
              from comparing incomparable elements.
            * False : Do not sort the result.

            .. versionadded:: 0.24.0

            .. versionchanged:: 0.24.1

               Changed the default value from ``True`` to ``None``
               (without change in behaviour).

        Returns
        -------
        difference : Index

        Examples
        --------

        >>> idx1 = pd.Index([2, 1, 3, 4])
        >>> idx2 = pd.Index([3, 4, 5, 6])
        >>> idx1.difference(idx2)
        Int64Index([1, 2], dtype='int64')
        >>> idx1.difference(idx2, sort=False)
        Int64Index([2, 1], dtype='int64')
        """
        self._validate_sort_keyword(sort)
        self._assert_can_do_setop(other)

        if self.equals(other):
            # pass an empty np.ndarray with the appropriate dtype
            return self._shallow_copy(self._data[:0])

        other, result_name = self._convert_can_do_setop(other)

        this = self._get_unique_index()

        indexer = this.get_indexer(other)
        indexer = indexer.take((indexer != -1).nonzero()[0])

        label_diff = np.setdiff1d(np.arange(this.size), indexer, assume_unique=True)
        the_diff = this.values.take(label_diff)
        if sort is None:
            try:
                the_diff = sorting.safe_sort(the_diff)
            except TypeError:
                pass

        return this._shallow_copy(the_diff, name=result_name, freq=None)
