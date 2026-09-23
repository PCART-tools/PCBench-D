    def _create_from_codes(self, codes, dtype=None, name=None):
        """
        *this is an internal non-public method*

        create the correct categorical from codes

        Parameters
        ----------
        codes : new codes
        dtype: CategoricalDtype, defaults to existing
        name : optional name attribute, defaults to existing

        Returns
        -------
        CategoricalIndex
        """

        if dtype is None:
            dtype = self.dtype
        if name is None:
            name = self.name
        cat = Categorical.from_codes(codes, dtype=dtype)
        return CategoricalIndex(cat, name=name)
