    @cache_readonly
    def is_unique(self):
        return self._engine.is_unique
