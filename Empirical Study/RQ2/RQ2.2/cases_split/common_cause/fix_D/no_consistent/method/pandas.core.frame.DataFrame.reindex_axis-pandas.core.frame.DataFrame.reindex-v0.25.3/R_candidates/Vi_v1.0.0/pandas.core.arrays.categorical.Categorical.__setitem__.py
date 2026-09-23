    def __setitem__(self, key, value):
        """
        Item assignment.

        Raises
        ------
        ValueError
            If (one or more) Value is not in categories or if a assigned
            `Categorical` does not have the same categories
        """
        value = extract_array(value, extract_numpy=True)

        # require identical categories set
        if isinstance(value, Categorical):
            if not is_dtype_equal(self, value):
                raise ValueError(
                    "Cannot set a Categorical with another, "
                    "without identical categories"
                )
            if not self.categories.equals(value.categories):
                new_codes = _recode_for_categories(
                    value.codes, value.categories, self.categories
                )
                value = Categorical.from_codes(new_codes, dtype=self.dtype)

        rvalue = value if is_list_like(value) else [value]

        from pandas import Index

        to_add = Index(rvalue).difference(self.categories)

        # no assignments of values not in categories, but it's always ok to set
        # something to np.nan
        if len(to_add) and not isna(to_add).all():
            raise ValueError(
                "Cannot setitem on a Categorical with a new "
                "category, set the categories first"
            )

        # set by position
        if isinstance(key, (int, np.integer)):
            pass

        # tuple of indexers (dataframe)
        elif isinstance(key, tuple):
            # only allow 1 dimensional slicing, but can
            # in a 2-d case be passd (slice(None),....)
            if len(key) == 2:
                if not com.is_null_slice(key[0]):
                    raise AssertionError("invalid slicing for a 1-ndim categorical")
                key = key[1]
            elif len(key) == 1:
                key = key[0]
            else:
                raise AssertionError("invalid slicing for a 1-ndim categorical")

        # slicing in Series or Categorical
        elif isinstance(key, slice):
            pass

        # else: array of True/False in Series or Categorical

        lindexer = self.categories.get_indexer(rvalue)
        lindexer = self._maybe_coerce_indexer(lindexer)
        self._codes[key] = lindexer
