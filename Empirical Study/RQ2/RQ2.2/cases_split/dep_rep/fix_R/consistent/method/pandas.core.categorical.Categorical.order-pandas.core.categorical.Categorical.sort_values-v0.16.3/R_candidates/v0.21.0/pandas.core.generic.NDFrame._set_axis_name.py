    def _set_axis_name(self, name, axis=0, inplace=False):
        """
        Alter the name or names of the axis.

        Parameters
        ----------
        name : str or list of str
            Name for the Index, or list of names for the MultiIndex
        axis : int or str
           0 or 'index' for the index; 1 or 'columns' for the columns
        inplace : bool
            whether to modify `self` directly or return a copy

            .. versionadded: 0.21.0

        Returns
        -------
        renamed : type of caller or None if inplace=True

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

        inplace = validate_bool_kwarg(inplace, 'inplace')
        renamed = self if inplace else self.copy()
        renamed.set_axis(idx, axis=axis, inplace=True)
        if not inplace:
            return renamed
