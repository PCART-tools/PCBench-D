    @cache_readonly
    def result_index(self) -> Index:
        # result_index retains dtype for categories, including unobserved ones,
        #  which group_index does not
        if self._all_grouper is not None:
            group_idx = self.group_index
            assert isinstance(group_idx, CategoricalIndex)
            return recode_from_groupby(self._all_grouper, self._sort, group_idx)
        return self.group_index
