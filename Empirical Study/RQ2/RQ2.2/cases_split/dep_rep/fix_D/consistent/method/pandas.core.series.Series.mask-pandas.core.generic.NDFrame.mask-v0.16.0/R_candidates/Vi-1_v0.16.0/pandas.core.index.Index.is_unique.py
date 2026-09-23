    @cache_readonly(allow_setting=True)
    def is_unique(self):
        """ return if the index has unique values """
        return self._engine.is_unique
