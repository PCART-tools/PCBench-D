    @cache_readonly
    def is_extension(self) -> bool:  # type: ignore[override]
        # i.e. datetime64tz, PeriodDtype
        return not isinstance(self.dtype, np.dtype)
