    @cache_readonly
    def is_unique(self):
        """
        Return if the index has unique values.
        """
        return self._engine.is_unique
