    @cache_readonly
    def _codes_and_uniques(self) -> tuple[npt.NDArray[np.signedinteger], ArrayLike]:
        if self._dropna and self._passed_categorical:
            # we make a CategoricalIndex out of the cat grouper
            # preserving the categories / ordered attributes;
            # doesn't (yet - GH#46909) handle dropna=False
            cat = self.grouping_vector
            categories = cat.categories

            if self._observed:
                ucodes = algorithms.unique1d(cat.codes)
                ucodes = ucodes[ucodes != -1]
                if self._sort or cat.ordered:
                    ucodes = np.sort(ucodes)
            else:
                ucodes = np.arange(len(categories))

            uniques = Categorical.from_codes(
                codes=ucodes, categories=categories, ordered=cat.ordered
            )
            return cat.codes, uniques

        elif isinstance(self.grouping_vector, ops.BaseGrouper):
            # we have a list of groupers
            codes = self.grouping_vector.codes_info
            # error: Incompatible types in assignment (expression has type "Union
            # [ExtensionArray, ndarray[Any, Any]]", variable has type "Categorical")
            uniques = (
                self.grouping_vector.result_index._values  # type: ignore[assignment]
            )
        else:
            # GH35667, replace dropna=False with use_na_sentinel=False
            # error: Incompatible types in assignment (expression has type "Union[
            # ndarray[Any, Any], Index]", variable has type "Categorical")
            codes, uniques = algorithms.factorize(  # type: ignore[assignment]
                self.grouping_vector, sort=self._sort, use_na_sentinel=self._dropna
            )
        return codes, uniques
