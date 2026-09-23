    def _get_level_values(self, level):
        """
        Return vector of label values for requested level,
        equal to the length of the index

        **this is an internal method**

        Parameters
        ----------
        level : int level

        Returns
        -------
        values : ndarray
        """

        unique = self.levels[level]
        labels = self.labels[level]
        filled = algos.take_1d(unique._values, labels,
                               fill_value=unique._na_value)
        values = unique._shallow_copy(filled)
        return values
