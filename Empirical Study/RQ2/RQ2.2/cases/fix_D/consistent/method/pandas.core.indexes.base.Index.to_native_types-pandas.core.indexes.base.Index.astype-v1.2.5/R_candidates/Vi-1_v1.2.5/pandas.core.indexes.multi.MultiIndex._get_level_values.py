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
        lev = self.levels[level]
        level_codes = self.codes[level]
        name = self._names[level]
        if unique:
            level_codes = algos.unique(level_codes)
        filled = algos.take_1d(lev._values, level_codes, fill_value=lev._na_value)
        return lev._shallow_copy(filled, name=name)
