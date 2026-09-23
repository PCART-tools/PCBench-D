    def unique(self):
        """
        Return array of unique values in the Index. Significantly faster than
        numpy.unique

        Returns
        -------
        uniques : ndarray
        """
        from pandas.core.nanops import unique1d
        return unique1d(self.values)
