    def isin(self, values, level=None):
        """
        Compute boolean array of whether each index value is found in the
        passed set of values

        Parameters
        ----------
        values : set or sequence of values
            Sought values.
        level : str or int, optional
            Name or position of the index level to use (if the index is a
            MultiIndex).

        Notes
        -----
        If `level` is specified:

        - if it is the name of one *and only one* index level, use that level;
        - otherwise it should be a number indicating level position.

        Returns
        -------
        is_contained : ndarray (boolean dtype)

        """
        value_set = set(values)
        if level is not None:
            self._validate_index_level(level)
        return lib.ismember(self._array_values(), value_set)
