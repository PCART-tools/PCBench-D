    def get_values(self):
        """
        Return the values.

        For internal compatibility with pandas formatting.

        Returns
        -------
        values : numpy array
            A numpy array of the same dtype as categorical.categories.dtype or
            Index if datetime / periods
        """
        # if we are a datetime and period index, return Index to keep metadata
        if is_datetimelike(self.categories):
            return self.categories.take(self._codes, fill_value=np.nan)
        elif is_integer_dtype(self.categories) and -1 in self._codes:
            return self.categories.astype("object").take(self._codes,
                                                         fill_value=np.nan)
        return np.array(self)
