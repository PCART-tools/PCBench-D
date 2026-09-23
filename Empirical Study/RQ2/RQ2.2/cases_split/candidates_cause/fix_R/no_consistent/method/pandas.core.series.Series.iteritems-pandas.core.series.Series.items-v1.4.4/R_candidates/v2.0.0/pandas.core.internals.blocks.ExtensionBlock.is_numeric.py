    @cache_readonly
    def is_numeric(self):
        return self.values.dtype._is_numeric
