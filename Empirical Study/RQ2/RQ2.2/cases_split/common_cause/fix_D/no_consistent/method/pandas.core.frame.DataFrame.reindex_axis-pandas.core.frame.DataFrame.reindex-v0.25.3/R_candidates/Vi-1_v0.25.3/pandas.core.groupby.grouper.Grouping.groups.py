    @cache_readonly
    def groups(self):
        return self.index.groupby(Categorical.from_codes(self.labels, self.group_index))
