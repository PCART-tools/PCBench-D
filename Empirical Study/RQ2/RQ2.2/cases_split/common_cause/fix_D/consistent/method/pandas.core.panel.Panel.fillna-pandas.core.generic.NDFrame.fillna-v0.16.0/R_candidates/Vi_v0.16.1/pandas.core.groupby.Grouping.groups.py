    @cache_readonly
    def groups(self):
        return self.index.groupby(self.grouper)
