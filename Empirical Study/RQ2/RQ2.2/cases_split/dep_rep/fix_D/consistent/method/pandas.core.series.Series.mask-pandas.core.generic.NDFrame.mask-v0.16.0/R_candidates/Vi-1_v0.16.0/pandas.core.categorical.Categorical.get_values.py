    def get_values(self):
        """ Return the values.

        For internal compatibility with pandas formatting.

        Returns
        -------
        values : numpy array
            A numpy array of the same dtype as categorical.categories.dtype or dtype string if
            periods
        """

        # if we are a period index, return a string repr
        if isinstance(self.categories, PeriodIndex):
            return take_1d(np.array(self.categories.to_native_types(), dtype=object),
                           self._codes)

        return np.array(self)
