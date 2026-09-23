    @cache_readonly
    def result_index(self) -> Index:
        if self.all_grouper is not None:
            return recode_from_groupby(self.all_grouper, self.sort, self.group_index)
        return self.group_index
