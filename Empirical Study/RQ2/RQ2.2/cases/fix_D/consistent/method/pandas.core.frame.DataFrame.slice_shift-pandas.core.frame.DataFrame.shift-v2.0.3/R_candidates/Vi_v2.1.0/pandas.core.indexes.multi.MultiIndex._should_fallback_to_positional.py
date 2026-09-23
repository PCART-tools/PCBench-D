    @cache_readonly
    def _should_fallback_to_positional(self) -> bool:
        """
        Should integer key(s) be treated as positional?
        """
        # GH#33355
        return self.levels[0]._should_fallback_to_positional
