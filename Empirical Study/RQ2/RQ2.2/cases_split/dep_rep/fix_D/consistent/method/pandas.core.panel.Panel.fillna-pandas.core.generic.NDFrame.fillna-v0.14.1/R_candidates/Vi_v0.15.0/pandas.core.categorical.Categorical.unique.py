    def unique(self):
        """
        Return the unique values.

        This includes all categories, even if one or more is unused.

        Returns
        -------
        unique values : array
        """
        return np.asarray(self.categories)
