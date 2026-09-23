    @cache_readonly
    def _codes_and_uniques(self) -> tuple[npt.NDArray[np.signedinteger], ArrayLike]:
        uniques: ArrayLike
        if self._passed_categorical:
            # we make a CategoricalIndex out of the cat grouper
            # preserving the categories / ordered attributes;
            # doesn't (yet - GH#46909) handle dropna=False
            cat = self.grouping_vector
            categories = cat.categories

            if self._observed:
                ucodes = algorithms.unique1d(cat.codes)
                ucodes = ucodes[ucodes != -1]
                if self._sort:
                    ucodes = np.sort(ucodes)
            else:
                ucodes = np.arange(len(categories))

            uniques = Categorical.from_codes(
                codes=ucodes, categories=categories, ordered=cat.ordered, validate=False
            )

            codes = cat.codes
            if not self._dropna:
                na_mask = codes < 0
                if np.any(na_mask):
                    if self._sort:
                        # Replace NA codes with `largest code + 1`
                        na_code = len(categories)
                        codes = np.where(na_mask, na_code, codes)
                    else:
                        # Insert NA code into the codes based on first appearance
                        # A negative code must exist, no need to check codes[na_idx] < 0
                        na_idx = na_mask.argmax()
                        # count number of unique codes that comes before the nan value
                        na_code = algorithms.nunique_ints(codes[:na_idx])
                        codes = np.where(codes >= na_code, codes + 1, codes)
                        codes = np.where(na_mask, na_code, codes)

            if not self._observed:
                uniques = uniques.reorder_categories(self._orig_cats)

            return codes, uniques

        elif isinstance(self.grouping_vector, ops.BaseGrouper):
            # we have a list of groupers
            codes = self.grouping_vector.codes_info
            uniques = self.grouping_vector.result_index._values
        elif self._uniques is not None:
            # GH#50486 Code grouping_vector using _uniques; allows
            # including uniques that are not present in grouping_vector.
            cat = Categorical(self.grouping_vector, categories=self._uniques)
            codes = cat.codes
            uniques = self._uniques
        else:
            # GH35667, replace dropna=False with use_na_sentinel=False
            # error: Incompatible types in assignment (expression has type "Union[
            # ndarray[Any, Any], Index]", variable has type "Categorical")
            codes, uniques = algorithms.factorize(  # type: ignore[assignment]
                self.grouping_vector, sort=self._sort, use_na_sentinel=self._dropna
            )
        return codes, uniques
