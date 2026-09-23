    def unstack(self, level=-1):
        """
        Pivot a level of the (necessarily hierarchical) index labels, returning
        a DataFrame having a new level of column labels whose inner-most level
        consists of the pivoted index labels. If the index is not a MultiIndex,
        the output will be a Series (the analogue of stack when the columns are
        not a MultiIndex)

        Parameters
        ----------
        level : int, string, or list of these, default -1 (last level)
            Level(s) of index to unstack, can pass level name

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
        one  a   1
             b   2
        two  a   3
             b   4
        dtype: float64

        >>> s.unstack(level=-1)
             a   b
        one  1  2
        two  3  4

        >>> s.unstack(level=0)
           one  two
        a  1   3
        b  2   4

        >>> df = s.unstack(level=0)
        >>> df.unstack()
        one  a  1.
             b  3.
        two  a  2.
             b  4.

        Returns
        -------
        unstacked : DataFrame or Series
        """
        from pandas.core.reshape import unstack
        return unstack(self, level)
