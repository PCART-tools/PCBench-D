    def _get_level_values(self, level, unique=False):
        """
        Return vector of label values for requested level,
        equal to the length of the index

        **this is an internal method**

        Parameters
        ----------
        level : int level
        unique : bool, default False
            if True, drop duplicated values

        Returns
        -------
        values : ndarray
        """

        values = self.levels[level]
        level_codes = self.codes[level]
        if unique:
            level_codes = algos.unique(level_codes)
        filled = algos.take_1d(values._values, level_codes, fill_value=values._na_value)
        values = values._shallow_copy(filled)
        return values
