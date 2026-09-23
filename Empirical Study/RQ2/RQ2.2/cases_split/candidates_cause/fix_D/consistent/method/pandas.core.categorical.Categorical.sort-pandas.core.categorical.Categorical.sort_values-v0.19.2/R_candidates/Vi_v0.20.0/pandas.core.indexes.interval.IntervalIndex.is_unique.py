    @cache_readonly
    def is_unique(self):
        return self._multiindex.is_unique
