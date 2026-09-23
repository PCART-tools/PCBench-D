    def unstack(self, level=-1, fill_value=None):
        """
        Pivot a level of the (necessarily hierarchical) index labels, returning
        a DataFrame having a new level of column labels whose inner-most level
        consists of the pivoted index labels. If the index is not a MultiIndex,
        the output will be a Series (the analogue of stack when the columns are
        not a MultiIndex).
        The level involved will automatically get sorted.

        Parameters
        ----------
        level : int, string, or list of these, default -1 (last level)
            Level(s) of index to unstack, can pass level name
        fill_value : replace NaN with this value if the unstack produces
            missing values

            .. versionadded: 0.18.0

        See also
        --------
        DataFrame.pivot : Pivot a table based on column values.
        DataFrame.stack : Pivot a level of the column labels (inverse operation
            from `unstack`).

        Examples
        --------
        >>> index = pd.MultiIndex.from_tuples([('one', 'a'), ('one', 'b'),
        ...                                    ('two', 'a'), ('two', 'b')])
        >>> s = pd.Series(np.arange(1.0, 5.0), index=index)
        >>> s
        one  a   1.0
             b   2.0
        two  a   3.0
             b   4.0
        dtype: float64

        >>> s.unstack(level=-1)
             a   b
        one  1.0  2.0
        two  3.0  4.0

        >>> s.unstack(level=0)
           one  two
        a  1.0   3.0
        b  2.0   4.0

        >>> df = s.unstack(level=0)
        >>> df.unstack()
        one  a  1.0
             b  2.0
        two  a  3.0
             b  4.0
        dtype: float64

        Returns
        -------
        unstacked : DataFrame or Series
        """
        from pandas.core.reshape.reshape import unstack
        return unstack(self, level, fill_value)
