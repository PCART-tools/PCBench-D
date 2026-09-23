    def _values_for_rank(self):
        """
        For correctly ranking ordered categorical data. See GH#15420

        Ordered categorical data should be ranked on the basis of
        codes with -1 translated to NaN.

        Returns
        -------
        numpy array

        """
        from pandas import Series
        if self.ordered:
            values = self.codes
            mask = values == -1
            if mask.any():
                values = values.astype('float64')
                values[mask] = np.nan
        elif self.categories.is_numeric():
            values = np.array(self)
        else:
            #  reorder the categories (so rank can use the float codes)
            #  instead of passing an object array to rank
            values = np.array(
                self.rename_categories(Series(self.categories).rank())
            )
        return values
