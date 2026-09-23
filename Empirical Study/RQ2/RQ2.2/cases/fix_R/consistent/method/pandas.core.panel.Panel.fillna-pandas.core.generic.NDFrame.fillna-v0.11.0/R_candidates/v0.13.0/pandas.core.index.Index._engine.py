    @cache_readonly
    def _engine(self):
        # property, for now, slow to look up
        return self._engine_type(lambda: self.values, len(self))
