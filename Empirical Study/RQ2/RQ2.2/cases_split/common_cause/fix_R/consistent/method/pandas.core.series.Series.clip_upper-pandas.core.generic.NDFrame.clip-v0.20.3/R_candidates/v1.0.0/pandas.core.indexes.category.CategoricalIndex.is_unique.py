    @cache_readonly
    def is_unique(self) -> bool:
        return self._engine.is_unique
