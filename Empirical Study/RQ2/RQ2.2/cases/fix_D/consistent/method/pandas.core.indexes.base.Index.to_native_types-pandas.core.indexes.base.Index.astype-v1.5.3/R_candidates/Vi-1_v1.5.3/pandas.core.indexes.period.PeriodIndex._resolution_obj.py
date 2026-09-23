    @cache_readonly
    # Signature of "_resolution_obj" incompatible with supertype "DatetimeIndexOpsMixin"
    def _resolution_obj(self) -> Resolution:  # type: ignore[override]
        # for compat with DatetimeIndex
        return self.dtype._resolution_obj
