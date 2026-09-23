    def unique(self):
        """
        Return array of unique values in the object. Significantly faster than
        numpy.unique. Includes NA values.

        Returns
        -------
        uniques : ndarray
        """
        from pandas.core.nanops import unique1d
        return unique1d(self.values)
