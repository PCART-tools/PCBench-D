    def isin(self, values, level=None):
        """
        Compute boolean array of whether each index value is found in the
        passed set of values.

        Parameters
        ----------
        values : set or list-like
            Sought values.

            .. versionadded:: 0.18.1

            Support for values as a set

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
        if level is not None:
            self._validate_index_level(level)
        return algos.isin(np.array(self), values)
