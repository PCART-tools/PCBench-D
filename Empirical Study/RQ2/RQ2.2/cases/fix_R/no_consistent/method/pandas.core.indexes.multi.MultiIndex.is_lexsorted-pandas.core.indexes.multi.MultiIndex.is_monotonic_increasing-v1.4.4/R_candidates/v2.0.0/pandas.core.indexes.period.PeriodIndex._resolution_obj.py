    @cache_readonly
    def _resolution_obj(self) -> Resolution:
        # for compat with DatetimeIndex
        return self.dtype._resolution_obj
