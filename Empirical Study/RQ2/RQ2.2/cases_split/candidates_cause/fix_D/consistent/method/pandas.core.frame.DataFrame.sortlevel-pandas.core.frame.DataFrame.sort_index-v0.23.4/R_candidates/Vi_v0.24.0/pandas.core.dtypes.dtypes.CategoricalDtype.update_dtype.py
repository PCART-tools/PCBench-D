    def update_dtype(self, dtype):
        """
        Returns a CategoricalDtype with categories and ordered taken from dtype
        if specified, otherwise falling back to self if unspecified

        Parameters
        ----------
        dtype : CategoricalDtype

        Returns
        -------
        new_dtype : CategoricalDtype
        """
        if isinstance(dtype, compat.string_types) and dtype == 'category':
            # dtype='category' should not change anything
            return self
        elif not self.is_dtype(dtype):
            msg = ('a CategoricalDtype must be passed to perform an update, '
                   'got {dtype!r}').format(dtype=dtype)
            raise ValueError(msg)
        elif dtype.categories is not None and dtype.ordered is self.ordered:
            return dtype

        # dtype is CDT: keep current categories/ordered if None
        new_categories = dtype.categories
        if new_categories is None:
            new_categories = self.categories

        new_ordered = dtype.ordered
        if new_ordered is None:
            new_ordered = self.ordered

        return CategoricalDtype(new_categories, new_ordered)
