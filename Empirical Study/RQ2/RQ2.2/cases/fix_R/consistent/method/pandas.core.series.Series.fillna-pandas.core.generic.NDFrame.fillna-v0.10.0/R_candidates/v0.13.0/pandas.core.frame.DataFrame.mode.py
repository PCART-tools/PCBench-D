    def mode(self, axis=0, numeric_only=False):
        """
        Gets the mode of each element along the axis selected. Empty if nothing
        has 2+ occurrences. Adds a row for each mode per label, fills in gaps
        with nan.

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
        """
        data = self if not numeric_only else self._get_numeric_data()
        f = lambda s: s.mode()
        return data.apply(f, axis=axis)
