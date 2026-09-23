    @cache_readonly
    def _can_hold_strings(self) -> bool:
        return not is_numeric_dtype(self.dtype)
