    def nlargest(self, n, columns, keep='first'):
        """Get the rows of a DataFrame sorted by the `n` largest
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
        >>> df.nlargest(3, 'a')
            a  b   c
        3  11  c   3
        1  10  b   2
        2   8  d NaN
        """
        return algos.select_n_frame(self, columns, n, 'nlargest', keep)
