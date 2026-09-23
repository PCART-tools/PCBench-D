    def mode(self, axis=0, numeric_only=False):
        """
        Gets the mode(s) of each element along the axis selected. Empty if nothing
        has 2+ occurrences. Adds a row for each mode per label, fills in gaps
        with nan.

        Note that there could be multiple values returned for the selected
        axis (when more than one item share the maximum frequency), which is the
        reason why a dataframe is returned. If you want to impute missing values
        with the mode in a dataframe ``df``, you can just do this:
        ``df.fillna(df.mode().iloc[0])``

        Parameters
        ----------
        axis : {0, 1, 'index', 'columns'} (default 0)
            * 0/'index' : get mode of each column
            * 1/'columns' : get mode of each row
        numeric_only : boolean, default False
            if True, only apply to numeric columns

        Returns
        -------
        modes : DataFrame (sorted)

        Examples
        --------
        >>> df = pd.DataFrame({'A': [1, 2, 1, 2, 1, 2, 3]})
        >>> df.mode()
           A
        0  1
        1  2
        """
        data = self if not numeric_only else self._get_numeric_data()
        f = lambda s: s.mode()
        return data.apply(f, axis=axis)
