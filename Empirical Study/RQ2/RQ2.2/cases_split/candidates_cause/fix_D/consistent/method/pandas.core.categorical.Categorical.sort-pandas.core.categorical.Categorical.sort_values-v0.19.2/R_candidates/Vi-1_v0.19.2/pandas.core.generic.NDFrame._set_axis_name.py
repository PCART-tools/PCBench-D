    def _set_axis_name(self, name, axis=0):
        """
        Alter the name or names of the axis, returning self.

        Parameters
        ----------
        name : str or list of str
            Name for the Index, or list of names for the MultiIndex
        axis : int or str
           0 or 'index' for the index; 1 or 'columns' for the columns

        Returns
        -------
        renamed : type of caller

        See Also
        --------
        pandas.DataFrame.rename
        pandas.Series.rename
        pandas.Index.rename

        Examples
        --------
        >>> df._set_axis_name("foo")
             A
        foo
        0    1
        1    2
        2    3
        >>> df.index = pd.MultiIndex.from_product([['A'], ['a', 'b', 'c']])
        >>> df._set_axis_name(["bar", "baz"])
                 A
        bar baz
        A   a    1
            b    2
            c    3
        """
        axis = self._get_axis_number(axis)
        idx = self._get_axis(axis).set_names(name)

        renamed = self.copy(deep=True)
        renamed.set_axis(axis, idx)
        return renamed
