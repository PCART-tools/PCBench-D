    @cache_readonly
    def _codes_and_uniques(self) -> tuple[np.ndarray, ArrayLike]:
        if self._passed_categorical:
            # we make a CategoricalIndex out of the cat grouper
            # preserving the categories / ordered attributes
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
            uniques = self.grouping_vector.result_arraylike
        else:
            # GH35667, replace dropna=False with na_sentinel=None
            if not self._dropna:
                na_sentinel = None
            else:
                na_sentinel = -1
            codes, uniques = algorithms.factorize(
                self.grouping_vector, sort=self._sort, na_sentinel=na_sentinel
            )
        return codes, uniques
