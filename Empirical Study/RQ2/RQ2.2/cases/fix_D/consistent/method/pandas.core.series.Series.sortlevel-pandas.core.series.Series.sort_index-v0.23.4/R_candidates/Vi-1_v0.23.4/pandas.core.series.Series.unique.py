    def unique(self):
        """
        Return unique values of Series object.

        Uniques are returned in order of appearance. Hash table-based unique,
        therefore does NOT sort.

        Returns
        -------
        ndarray or Categorical
            The unique values returned as a NumPy array. In case of categorical
            data type, returned as a Categorical.

        See Also
        --------
        pandas.unique : top-level unique method for any 1-d array-like object.
        Index.unique : return Index with unique values from an Index object.

        Examples
        --------
        >>> pd.Series([2, 1, 3, 3], name='A').unique()
        array([2, 1, 3])

        >>> pd.Series([pd.Timestamp('2016-01-01') for _ in range(3)]).unique()
        array(['2016-01-01T00:00:00.000000000'], dtype='datetime64[ns]')

        >>> pd.Series([pd.Timestamp('2016-01-01', tz='US/Eastern')
        ...            for _ in range(3)]).unique()
        array([Timestamp('2016-01-01 00:00:00-0500', tz='US/Eastern')],
              dtype=object)

        An unordered Categorical will return categories in the order of
        appearance.

        >>> pd.Series(pd.Categorical(list('baabc'))).unique()
        [b, a, c]
        Categories (3, object): [b, a, c]

        An ordered Categorical preserves the category ordering.

        >>> pd.Series(pd.Categorical(list('baabc'), categories=list('abc'),
        ...                          ordered=True)).unique()
        [b, a, c]
        Categories (3, object): [a < b < c]
        """
        result = super(Series, self).unique()

        if is_datetime64tz_dtype(self.dtype):
            # we are special casing datetime64tz_dtype
            # to return an object array of tz-aware Timestamps

            # TODO: it must return DatetimeArray with tz in pandas 2.0
            result = result.astype(object).values

        return result
