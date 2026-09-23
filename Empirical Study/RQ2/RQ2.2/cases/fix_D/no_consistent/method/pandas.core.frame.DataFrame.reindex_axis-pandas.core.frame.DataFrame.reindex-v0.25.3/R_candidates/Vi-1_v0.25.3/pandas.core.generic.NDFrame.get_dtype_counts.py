    def get_dtype_counts(self):
        """
        Return counts of unique dtypes in this object.

        .. deprecated:: 0.25.0

        Use `.dtypes.value_counts()` instead.

        Returns
        -------
        dtype : Series
            Series with the count of columns with each dtype.

        See Also
        --------
        dtypes : Return the dtypes in this object.

        Examples
        --------
        >>> a = [['a', 1, 1.0], ['b', 2, 2.0], ['c', 3, 3.0]]
        >>> df = pd.DataFrame(a, columns=['str', 'int', 'float'])
        >>> df
          str  int  float
        0   a    1    1.0
        1   b    2    2.0
        2   c    3    3.0

        >>> df.get_dtype_counts()
        float64    1
        int64      1
        object     1
        dtype: int64
        """
        warnings.warn(
            "`get_dtype_counts` has been deprecated and will be "
            "removed in a future version. For DataFrames use "
            "`.dtypes.value_counts()",
            FutureWarning,
            stacklevel=2,
        )

        from pandas import Series

        return Series(self._data.get_dtype_counts())
