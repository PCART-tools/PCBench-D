    @cache_readonly
    def _can_hold_na(self) -> bool:  # type: ignore[override]
        if is_float_dtype(self.dtype):
            return True
        else:
            return False
