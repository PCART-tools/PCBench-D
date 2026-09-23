    @cache_readonly
    def _have_mixed_levels(self):
        """ return a boolean list indicated if we have mixed levels """
        return ['mixed' in l for l in self._inferred_type_levels]
