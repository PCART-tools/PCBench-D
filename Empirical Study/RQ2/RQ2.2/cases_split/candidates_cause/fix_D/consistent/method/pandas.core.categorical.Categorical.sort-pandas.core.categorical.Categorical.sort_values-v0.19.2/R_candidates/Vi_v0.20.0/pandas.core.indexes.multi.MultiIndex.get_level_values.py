    def get_level_values(self, level):
        """
        Return vector of label values for requested level,
        equal to the length of the index

        Parameters
        ----------
        level : int or level name

        Returns
        -------
        values : Index
        """
        level = self._get_level_number(level)
        values = self._get_level_values(level)
        return values
