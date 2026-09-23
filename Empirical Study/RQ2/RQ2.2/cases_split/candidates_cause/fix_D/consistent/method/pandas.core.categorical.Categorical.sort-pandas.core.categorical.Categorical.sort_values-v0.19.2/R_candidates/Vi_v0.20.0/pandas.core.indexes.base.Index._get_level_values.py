    def _get_level_values(self, level):
        """
        Return an Index of values for requested level, equal to the length
        of the index

        Parameters
        ----------
        level : int

        Returns
        -------
        values : Index
        """

        self._validate_index_level(level)
        return self
