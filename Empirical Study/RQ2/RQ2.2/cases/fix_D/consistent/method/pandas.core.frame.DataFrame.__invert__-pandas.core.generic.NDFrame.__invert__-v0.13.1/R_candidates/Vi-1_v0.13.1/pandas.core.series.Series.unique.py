    def unique(self):
        """
        Return array of unique values in the Series. Significantly faster than
        numpy.unique

        Returns
        -------
        uniques : ndarray
        """
        return nanops.unique1d(self.values)
