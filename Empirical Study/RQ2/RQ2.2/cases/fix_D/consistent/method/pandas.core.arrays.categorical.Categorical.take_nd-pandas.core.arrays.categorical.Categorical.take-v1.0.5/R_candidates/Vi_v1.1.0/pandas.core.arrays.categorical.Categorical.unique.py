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

        See Also
        --------
        pandas.unique
        CategoricalIndex.unique
        Series.unique

        Examples
        --------
        An unordered Categorical will return categories in the
        order of appearance.

        >>> pd.Categorical(list("baabc")).unique()
        ['b', 'a', 'c']
        Categories (3, object): ['b', 'a', 'c']

        >>> pd.Categorical(list("baabc"), categories=list("abc")).unique()
        ['b', 'a', 'c']
        Categories (3, object): ['b', 'a', 'c']

        An ordered Categorical preserves the category ordering.

        >>> pd.Categorical(
        ...     list("baabc"), categories=list("abc"), ordered=True
        ... ).unique()
        ['b', 'a', 'c']
        Categories (3, object): ['a' < 'b' < 'c']
        """
        # unlike np.unique, unique1d does not sort
        unique_codes = unique1d(self.codes)
        cat = self.copy()

        # keep nan in codes
        cat._codes = unique_codes

        # exclude nan from indexer for categories
        take_codes = unique_codes[unique_codes != -1]
        if self.ordered:
            take_codes = np.sort(take_codes)
        return cat.set_categories(cat.categories.take(take_codes))
