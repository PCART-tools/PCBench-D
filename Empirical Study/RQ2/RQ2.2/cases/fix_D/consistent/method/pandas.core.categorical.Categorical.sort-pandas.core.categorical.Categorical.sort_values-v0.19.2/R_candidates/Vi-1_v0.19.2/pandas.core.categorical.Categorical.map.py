    def map(self, mapper):
        """
        Apply mapper function to its categories (not codes).

        Parameters
        ----------
        mapper : callable
            Function to be applied. When all categories are mapped
            to different categories, the result will be Categorical which has
            the same order property as the original. Otherwise, the result will
            be np.ndarray.

        Returns
        -------
        applied : Categorical or np.ndarray.
        """
        new_categories = self.categories.map(mapper)
        try:
            return self.from_codes(self._codes.copy(),
                                   categories=new_categories,
                                   ordered=self.ordered)
        except ValueError:
            return np.take(new_categories, self._codes)
