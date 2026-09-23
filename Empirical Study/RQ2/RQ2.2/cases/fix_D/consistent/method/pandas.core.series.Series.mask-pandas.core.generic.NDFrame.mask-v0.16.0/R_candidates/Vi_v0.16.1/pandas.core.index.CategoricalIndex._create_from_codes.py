    def _create_from_codes(self, codes, categories=None, ordered=None, name=None):
        """
        *this is an internal non-public method*

        create the correct categorical from codes

        Parameters
        ----------
        codes : new codes
        categories : optional categories, defaults to existing
        ordered : optional ordered attribute, defaults to existing
        name : optional name attribute, defaults to existing

        Returns
        -------
        CategoricalIndex
        """

        from pandas.core.categorical import Categorical
        if categories is None:
            categories = self.categories
        if ordered is None:
            ordered = self.ordered
        if name is None:
            name = self.name
        cat = Categorical.from_codes(codes, categories=categories, ordered=self.ordered)
        return CategoricalIndex(cat, name=name)
