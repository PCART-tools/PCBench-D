    def _validate_listlike(self, value):
        # NB: here we assume scalar-like tuples have already been excluded
        value = extract_array(value, extract_numpy=True)

        # require identical categories set
        if isinstance(value, Categorical):
            if self.dtype != value.dtype:
                raise TypeError(
                    "Cannot set a Categorical with another, "
                    "without identical categories"
                )
            # dtype equality implies categories_match_up_to_permutation
            value = self._encode_with_my_categories(value)
            return value._codes

        from pandas import Index

        # tupleize_cols=False for e.g. test_fillna_iterable_category GH#41914
        to_add = Index._with_infer(value, tupleize_cols=False).difference(
            self.categories
        )

        # no assignments of values not in categories, but it's always ok to set
        # something to np.nan
        if len(to_add) and not isna(to_add).all():
            raise TypeError(
                "Cannot setitem on a Categorical with a new "
                "category, set the categories first"
            )

        codes = self.categories.get_indexer(value)
        return codes.astype(self._ndarray.dtype, copy=False)
