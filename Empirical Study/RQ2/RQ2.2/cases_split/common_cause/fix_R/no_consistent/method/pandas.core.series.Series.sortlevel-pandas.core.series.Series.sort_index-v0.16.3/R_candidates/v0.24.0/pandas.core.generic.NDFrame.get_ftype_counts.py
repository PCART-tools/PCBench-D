    def get_ftype_counts(self):
        """
        Return counts of unique ftypes in this object.

        .. deprecated:: 0.23.0

        This is useful for SparseDataFrame or for DataFrames containing
        sparse arrays.

        Returns
        -------
        dtype : Series
            Series with the count of columns with each type and
            sparsity (dense/sparse)

        See Also
        --------
        ftypes : Return ftypes (indication of sparse/dense and dtype) in
            this object.

        Examples
        --------
        >>> a = [['a', 1, 1.0], ['b', 2, 2.0], ['c', 3, 3.0]]
        >>> df = pd.DataFrame(a, columns=['str', 'int', 'float'])
        >>> df
          str  int  float
        0   a    1    1.0
        1   b    2    2.0
        2   c    3    3.0

        >>> df.get_ftype_counts()  # doctest: +SKIP
        float64:dense    1
        int64:dense      1
        object:dense     1
        dtype: int64
        """
        warnings.warn("get_ftype_counts is deprecated and will "
                      "be removed in a future version",
                      FutureWarning, stacklevel=2)

        from pandas import Series
        return Series(self._data.get_ftype_counts())
