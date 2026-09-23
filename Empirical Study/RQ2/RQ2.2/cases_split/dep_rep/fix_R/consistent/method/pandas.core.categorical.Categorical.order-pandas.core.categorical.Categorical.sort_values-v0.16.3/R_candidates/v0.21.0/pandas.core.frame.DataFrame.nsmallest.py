    def nsmallest(self, n, columns, keep='first'):
        """Get the rows of a DataFrame sorted by the `n` smallest
        values of `columns`.

        .. versionadded:: 0.17.0

        Parameters
        ----------
        n : int
            Number of items to retrieve
        columns : list or str
            Column name or names to order by
        keep : {'first', 'last', False}, default 'first'
            Where there are duplicate values:
            - ``first`` : take the first occurrence.
            - ``last`` : take the last occurrence.

        Returns
        -------
        DataFrame

        Examples
        --------
        >>> df = DataFrame({'a': [1, 10, 8, 11, -1],
        ...                 'b': list('abdce'),
        ...                 'c': [1.0, 2.0, np.nan, 3.0, 4.0]})
        >>> df.nsmallest(3, 'a')
           a  b   c
        4 -1  e   4
        0  1  a   1
        2  8  d NaN
        """
        return algorithms.SelectNFrame(self,
                                       n=n,
                                       keep=keep,
                                       columns=columns).nsmallest()
