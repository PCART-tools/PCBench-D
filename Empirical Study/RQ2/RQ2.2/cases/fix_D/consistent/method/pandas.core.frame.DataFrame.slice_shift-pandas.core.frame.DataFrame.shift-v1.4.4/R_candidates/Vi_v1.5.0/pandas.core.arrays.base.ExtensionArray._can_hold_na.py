    @cache_readonly
    def _can_hold_na(self) -> bool:
        return self.dtype._can_hold_na
