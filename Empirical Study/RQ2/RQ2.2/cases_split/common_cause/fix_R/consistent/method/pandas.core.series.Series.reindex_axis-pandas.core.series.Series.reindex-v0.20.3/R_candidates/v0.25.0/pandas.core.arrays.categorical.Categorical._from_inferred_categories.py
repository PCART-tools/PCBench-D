    @classmethod
    def _from_inferred_categories(
        cls, inferred_categories, inferred_codes, dtype, true_values=None
    ):
        """
        Construct a Categorical from inferred values.

        For inferred categories (`dtype` is None) the categories are sorted.
        For explicit `dtype`, the `inferred_categories` are cast to the
        appropriate type.

        Parameters
        ----------
        inferred_categories : Index
        inferred_codes : Index
        dtype : CategoricalDtype or 'category'
        true_values : list, optional
            If none are provided, the default ones are
            "True", "TRUE", and "true."

        Returns
        -------
        Categorical
        """
        from pandas import Index, to_numeric, to_datetime, to_timedelta

        cats = Index(inferred_categories)
        known_categories = (
            isinstance(dtype, CategoricalDtype) and dtype.categories is not None
        )

        if known_categories:
            # Convert to a specialized type with `dtype` if specified.
            if dtype.categories.is_numeric():
                cats = to_numeric(inferred_categories, errors="coerce")
            elif is_datetime64_dtype(dtype.categories):
                cats = to_datetime(inferred_categories, errors="coerce")
            elif is_timedelta64_dtype(dtype.categories):
                cats = to_timedelta(inferred_categories, errors="coerce")
            elif dtype.categories.is_boolean():
                if true_values is None:
                    true_values = ["True", "TRUE", "true"]

                cats = cats.isin(true_values)

        if known_categories:
            # Recode from observation order to dtype.categories order.
            categories = dtype.categories
            codes = _recode_for_categories(inferred_codes, cats, categories)
        elif not cats.is_monotonic_increasing:
            # Sort categories and recode for unknown categories.
            unsorted = cats.copy()
            categories = cats.sort_values()

            codes = _recode_for_categories(inferred_codes, unsorted, categories)
            dtype = CategoricalDtype(categories, ordered=False)
        else:
            dtype = CategoricalDtype(cats, ordered=False)
            codes = inferred_codes

        return cls(codes, dtype=dtype, fastpath=True)
