    def get_duplicates(self):
        """
        Extract duplicated index elements.

        .. deprecated:: 0.23.0
            Use idx[idx.duplicated()].unique() instead

        Returns a sorted list of index elements which appear more than once in
        the index.

        Returns
        -------
        array-like
            List of duplicated indexes.

        See Also
        --------
        Index.duplicated : Return boolean array denoting duplicates.
        Index.drop_duplicates : Return Index with duplicates removed.

        Examples
        --------

        Works on different Index of types.

        >>> pd.Index([1, 2, 2, 3, 3, 3, 4]).get_duplicates()  # doctest: +SKIP
        [2, 3]

        Note that for a DatetimeIndex, it does not return a list but a new
        DatetimeIndex:

        >>> dates = pd.to_datetime(['2018-01-01', '2018-01-02', '2018-01-03',
        ...                         '2018-01-03', '2018-01-04', '2018-01-04'],
        ...                        format='%Y-%m-%d')
        >>> pd.Index(dates).get_duplicates()  # doctest: +SKIP
        DatetimeIndex(['2018-01-03', '2018-01-04'],
                      dtype='datetime64[ns]', freq=None)

        Sorts duplicated elements even when indexes are unordered.

        >>> pd.Index([1, 2, 3, 2, 3, 4, 3]).get_duplicates()  # doctest: +SKIP
        [2, 3]

        Return empty array-like structure when all elements are unique.

        >>> pd.Index([1, 2, 3, 4]).get_duplicates()  # doctest: +SKIP
        []
        >>> dates = pd.to_datetime(['2018-01-01', '2018-01-02', '2018-01-03'],
        ...                        format='%Y-%m-%d')
        >>> pd.Index(dates).get_duplicates()  # doctest: +SKIP
        DatetimeIndex([], dtype='datetime64[ns]', freq=None)
        """
        warnings.warn(
            "'get_duplicates' is deprecated and will be removed in "
            "a future release. You can use "
            "idx[idx.duplicated()].unique() instead",
            FutureWarning,
            stacklevel=2,
        )

        return self[self.duplicated()].unique()
