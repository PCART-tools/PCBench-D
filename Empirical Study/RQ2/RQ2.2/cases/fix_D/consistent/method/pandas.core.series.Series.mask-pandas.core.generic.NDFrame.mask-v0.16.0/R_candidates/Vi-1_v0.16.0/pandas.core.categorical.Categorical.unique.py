    def unique(self):
        """
        Return the unique values.

        Unused categories are NOT returned. Unique values are returned in order
        of appearance.

        Returns
        -------
        unique values : array
        """
        from pandas.core.nanops import unique1d
        # unlike np.unique, unique1d does not sort
        unique_codes = unique1d(self.codes)
        return take_1d(self.categories.values, unique_codes)
