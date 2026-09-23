    def explode(self) -> "Series":
        """
        Transform each element of a list-like to a row, replicating the
        index values.

        .. versionadded:: 0.25.0

        Returns
        -------
        Series
            Exploded lists to rows; index will be duplicated for these rows.

        See Also
        --------
        Series.str.split : Split string values on specified separator.
        Series.unstack : Unstack, a.k.a. pivot, Series with MultiIndex
            to produce DataFrame.
        DataFrame.melt : Unpivot a DataFrame from wide format to long format.
        DataFrame.explode : Explode a DataFrame from list-like
            columns to long format.

        Notes
        -----
        This routine will explode list-likes including lists, tuples,
        Series, and np.ndarray. The result dtype of the subset rows will
        be object. Scalars will be returned unchanged. Empty list-likes will
        result in a np.nan for that row.

        Examples
        --------
        >>> s = pd.Series([[1, 2, 3], 'foo', [], [3, 4]])
        >>> s
        0    [1, 2, 3]
        1          foo
        2           []
        3       [3, 4]
        dtype: object

        >>> s.explode()
        0      1
        0      2
        0      3
        1    foo
        2    NaN
        3      3
        3      4
        dtype: object
        """
        if not len(self) or not is_object_dtype(self):
            return self.copy()

        values, counts = reshape.explode(np.asarray(self.array))

        result = Series(values, index=self.index.repeat(counts), name=self.name)
        return result
