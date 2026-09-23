    def _get_level_values(self, level):
        """
        Return an Index of values for requested level, equal to the length
        of the index.

        Parameters
        ----------
        level : int or str
            ``level`` is either the integer position of the level in the
            MultiIndex, or the name of the level.

        Returns
        -------
        values : Index
            ``self``, as there is only one level in the Index.

        See also
        ---------
        pandas.MultiIndex.get_level_values : get values for a level of a
                                             MultiIndex
        """

        self._validate_index_level(level)
        return self
