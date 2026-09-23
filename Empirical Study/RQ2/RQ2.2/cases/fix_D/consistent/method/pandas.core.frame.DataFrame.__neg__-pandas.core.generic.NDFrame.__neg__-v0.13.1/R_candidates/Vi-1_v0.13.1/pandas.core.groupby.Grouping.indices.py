    @cache_readonly
    def indices(self):
        return _groupby_indices(self.grouper)
