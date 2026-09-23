    @cache_readonly
    def _engine(self):
        return self._engine_type(lambda: self, len(self))
