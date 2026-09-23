    def _set_dtype(self, dtype: CategoricalDtype) -> Self:
        """
        Internal method for directly updating the CategoricalDtype

        Parameters
        ----------
        dtype : CategoricalDtype

        Notes
        -----
        We don't do any validation here. It's assumed that the dtype is
        a (valid) instance of `CategoricalDtype`.
        """
        codes = recode_for_categories(self.codes, self.categories, dtype.categories)
        return type(self)._simple_new(codes, dtype=dtype)
