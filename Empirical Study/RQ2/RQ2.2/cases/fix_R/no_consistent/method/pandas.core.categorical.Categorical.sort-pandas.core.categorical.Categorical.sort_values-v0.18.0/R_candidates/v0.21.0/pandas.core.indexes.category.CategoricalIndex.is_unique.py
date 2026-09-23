    @cache_readonly
    def is_unique(self):
        return not self.duplicated().any()
