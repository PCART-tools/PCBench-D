    @cache_readonly(allow_setting=True)
    def is_unique(self):
        return self._engine.is_unique
