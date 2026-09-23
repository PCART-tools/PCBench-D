    def unstack(self, level=-1, fill_value=None):
        """
        Unstack, a.k.a. pivot, Series with MultiIndex to produce DataFrame.
        The level involved will automatically get sorted.

        Parameters
        ----------
        level : int, string, or list of these, default last level
            Level(s) to unstack, can pass level name
        fill_value : replace NaN with this value if the unstack produces
            missing values

            .. versionadded: 0.18.0

        Examples
        --------
        >>> s
        one  a   1.
        one  b   2.
        two  a   3.
        two  b   4.

        >>> s.unstack(level=-1)
             a   b
        one  1.  2.
        two  3.  4.

        >>> s.unstack(level=0)
           one  two
        a  1.   2.
        b  3.   4.

        Returns
        -------
        unstacked : DataFrame
        """
        from pandas.core.reshape import unstack
        return unstack(self, level, fill_value)
