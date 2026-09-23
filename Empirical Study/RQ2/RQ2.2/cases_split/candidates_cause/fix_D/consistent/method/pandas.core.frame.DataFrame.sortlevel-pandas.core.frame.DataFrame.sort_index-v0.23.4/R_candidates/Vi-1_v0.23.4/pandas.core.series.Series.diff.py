    def diff(self, periods=1):
        """
        First discrete difference of element.

        Calculates the difference of a Series element compared with another
        element in the Series (default is element in previous row).

        Parameters
        ----------
        periods : int, default 1
            Periods to shift for calculating difference, accepts negative
            values.

        Returns
        -------
        diffed : Series

        See Also
        --------
        Series.pct_change: Percent change over given number of periods.
        Series.shift: Shift index by desired number of periods with an
            optional time freq.
        DataFrame.diff: First discrete difference of object

        Examples
        --------
        Difference with previous row

        >>> s = pd.Series([1, 1, 2, 3, 5, 8])
        >>> s.diff()
        0    NaN
        1    0.0
        2    1.0
        3    1.0
        4    2.0
        5    3.0
        dtype: float64

        Difference with 3rd previous row

        >>> s.diff(periods=3)
        0    NaN
        1    NaN
        2    NaN
        3    2.0
        4    4.0
        5    6.0
        dtype: float64

        Difference with following row

        >>> s.diff(periods=-1)
        0    0.0
        1   -1.0
        2   -1.0
        3   -2.0
        4   -3.0
        5    NaN
        dtype: float64
        """
        result = algorithms.diff(com._values_from_object(self), periods)
        return self._constructor(result, index=self.index).__finalize__(self)
