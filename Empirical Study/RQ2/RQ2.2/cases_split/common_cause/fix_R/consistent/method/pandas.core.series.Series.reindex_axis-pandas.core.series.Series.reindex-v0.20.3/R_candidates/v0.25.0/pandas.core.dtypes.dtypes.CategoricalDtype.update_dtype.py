    def update_dtype(self, dtype: "CategoricalDtype") -> "CategoricalDtype":
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
        if isinstance(dtype, str) and dtype == "category":
            # dtype='category' should not change anything
            return self
        elif not self.is_dtype(dtype):
            msg = (
                "a CategoricalDtype must be passed to perform an update, "
                "got {dtype!r}"
            ).format(dtype=dtype)
            raise ValueError(msg)

        # dtype is CDT: keep current categories/ordered if None
        new_categories = dtype.categories
        if new_categories is None:
            new_categories = self.categories

        new_ordered = dtype._ordered
        new_ordered_from_sentinel = dtype._ordered_from_sentinel
        if new_ordered is None:
            # maintain existing ordered if new dtype has ordered=None
            new_ordered = self._ordered
            if self._ordered and new_ordered_from_sentinel:
                # only warn if we'd actually change the existing behavior
                msg = (
                    "Constructing a CategoricalDtype without specifying "
                    "`ordered` will default to `ordered=False` in a future "
                    "version, which will cause the resulting categorical's "
                    "`ordered` attribute to change to False; `ordered=True`"
                    " must be explicitly passed in order to be retained"
                )
                warnings.warn(msg, FutureWarning, stacklevel=3)

        return CategoricalDtype(new_categories, new_ordered)
