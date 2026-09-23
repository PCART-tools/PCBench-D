    @cache_readonly
    def result_index(self):
        if self.all_grouper is not None:
            from pandas.core.groupby.categorical import recode_from_groupby

            return recode_from_groupby(self.all_grouper, self.sort, self.group_index)
        return self.group_index
