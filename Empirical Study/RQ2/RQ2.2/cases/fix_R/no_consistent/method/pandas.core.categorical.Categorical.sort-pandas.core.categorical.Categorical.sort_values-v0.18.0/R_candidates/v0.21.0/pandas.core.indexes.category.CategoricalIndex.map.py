    def map(self, mapper):
        """Apply mapper function to its categories (not codes).

        Parameters
        ----------
        mapper : callable
            Function to be applied. When all categories are mapped
            to different categories, the result will be a CategoricalIndex
            which has the same order property as the original. Otherwise,
            the result will be a Index.

        Returns
        -------
        applied : CategoricalIndex or Index

        """
        return self._shallow_copy_with_infer(self.values.map(mapper))
