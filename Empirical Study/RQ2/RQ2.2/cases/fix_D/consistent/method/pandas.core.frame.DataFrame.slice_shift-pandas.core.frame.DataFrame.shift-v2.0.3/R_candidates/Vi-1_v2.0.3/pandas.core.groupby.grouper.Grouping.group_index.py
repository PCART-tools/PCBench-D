    @cache_readonly
    def group_index(self) -> Index:
        codes, uniques = self._codes_and_uniques
        if not self._dropna and self._passed_categorical:
            assert isinstance(uniques, Categorical)
            if self._sort and (codes == len(uniques)).any():
                # Add NA value on the end when sorting
                uniques = Categorical.from_codes(
                    np.append(uniques.codes, [-1]), uniques.categories
                )
            elif len(codes) > 0:
                # Need to determine proper placement of NA value when not sorting
                cat = self.grouping_vector
                na_idx = (cat.codes < 0).argmax()
                if cat.codes[na_idx] < 0:
                    # count number of unique codes that comes before the nan value
                    na_unique_idx = algorithms.nunique_ints(cat.codes[:na_idx])
                    uniques = Categorical.from_codes(
                        np.insert(uniques.codes, na_unique_idx, -1), uniques.categories
                    )
        return Index._with_infer(uniques, name=self.name)
