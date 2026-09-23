    def to_dense(self):
        """
        Convert a Series from sparse values to dense.

        .. versionadded:: 0.25.0

        Returns
        -------
        Series:
            A Series with the same values, stored as a dense array.

        Examples
        --------
        >>> series = pd.Series(pd.SparseArray([0, 1, 0]))
        >>> series
        0    0
        1    1
        2    0
        dtype: Sparse[int64, 0]

        >>> series.sparse.to_dense()
        0    0
        1    1
        2    0
        dtype: int64
        """
        from pandas import Series

        return Series(
            self._parent.array.to_dense(),
            index=self._parent.index,
            name=self._parent.name,
        )
