    def get_level_values(self, level):
        """
        Return vector of label values for requested level, equal to the length
        of the index

        Parameters
        ----------
        level : int

        Returns
        -------
        values : ndarray
        """
        # checks that level number is actually just 1
        self._get_level_number(level)
        return self
