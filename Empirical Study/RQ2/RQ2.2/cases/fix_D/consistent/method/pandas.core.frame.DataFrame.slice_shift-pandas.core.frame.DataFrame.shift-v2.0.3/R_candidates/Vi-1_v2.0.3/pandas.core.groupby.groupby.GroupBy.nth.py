    @final
    @property
    @Substitution(name="groupby")
    @Substitution(see_also=_common_see_also)
    def nth(self) -> GroupByNthSelector:
        """
        Take the nth row from each group if n is an int, otherwise a subset of rows.

        Can be either a call or an index. dropna is not available with index notation.
        Index notation accepts a comma separated list of integers and slices.

        If dropna, will take the nth non-null row, dropna is either
        'all' or 'any'; this is equivalent to calling dropna(how=dropna)
        before the groupby.

        Parameters
        ----------
        n : int, slice or list of ints and slices
            A single nth value for the row or a list of nth values or slices.

            .. versionchanged:: 1.4.0
                Added slice and lists containing slices.
                Added index notation.

        dropna : {'any', 'all', None}, default None
            Apply the specified dropna operation before counting which row is
            the nth row. Only supported if n is an int.

        Returns
        -------
        Series or DataFrame
            N-th value within each group.
        %(see_also)s
        Examples
        --------

        >>> df = pd.DataFrame({'A': [1, 1, 2, 1, 2],
        ...                    'B': [np.nan, 2, 3, 4, 5]}, columns=['A', 'B'])
        >>> g = df.groupby('A')
        >>> g.nth(0)
           A   B
        0  1 NaN
        2  2 3.0
        >>> g.nth(1)
           A   B
        1  1 2.0
        4  2 5.0
        >>> g.nth(-1)
           A   B
        3  1 4.0
        4  2 5.0
        >>> g.nth([0, 1])
           A   B
        0  1 NaN
        1  1 2.0
        2  2 3.0
        4  2 5.0
        >>> g.nth(slice(None, -1))
           A   B
        0  1 NaN
        1  1 2.0
        2  2 3.0

        Index notation may also be used

        >>> g.nth[0, 1]
           A   B
        0  1 NaN
        1  1 2.0
        2  2 3.0
        4  2 5.0
        >>> g.nth[:-1]
           A   B
        0  1 NaN
        1  1 2.0
        2  2 3.0

        Specifying `dropna` allows ignoring ``NaN`` values

        >>> g.nth(0, dropna='any')
           A   B
        1  1 2.0
        2  2 3.0

        When the specified ``n`` is larger than any of the groups, an
        empty DataFrame is returned

        >>> g.nth(3, dropna='any')
        Empty DataFrame
        Columns: [A, B]
        Index: []
        """
        return GroupByNthSelector(self)
