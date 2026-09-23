    def nunique(self, axis=0, dropna=True):
        """
        Return Series with number of distinct observations over requested
        axis.

        .. versionadded:: 0.20.0

        Parameters
        ----------
        axis : {0 or 'index', 1 or 'columns'}, default 0
        dropna : boolean, default True
            Don't include NaN in the counts.

        Returns
        -------
        nunique : Series

        Examples
        --------
        >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': [1, 1, 1]})
        >>> df.nunique()
        A    3
        B    1

        >>> df.nunique(axis=1)
        0    1
        1    2
        2    2
        """
        return self.apply(Series.nunique, axis=axis, dropna=dropna)
