    def unique(self):
        """
        Return the ``Categorical`` which ``categories`` and ``codes`` are
        unique. Unused categories are NOT returned.

        - unordered category: values and categories are sorted by appearance
          order.
        - ordered category: values are sorted by appearance order, categories
          keeps existing order.

        Returns
        -------
        unique values : ``Categorical``
        """

        from pandas.core.nanops import unique1d
        # unlike np.unique, unique1d does not sort
        unique_codes = unique1d(self.codes)
        cat = self.copy()
        # keep nan in codes
        cat._codes = unique_codes
        # exclude nan from indexer for categories
        take_codes = unique_codes[unique_codes != -1]
        if self.ordered:
            take_codes = sorted(take_codes)
        return cat.set_categories(cat.categories.take(take_codes))
