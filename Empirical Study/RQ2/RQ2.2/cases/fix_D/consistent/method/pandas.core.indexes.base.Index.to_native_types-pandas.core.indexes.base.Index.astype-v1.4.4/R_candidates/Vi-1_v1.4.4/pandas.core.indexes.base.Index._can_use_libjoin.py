    @cache_readonly
    def _can_use_libjoin(self) -> bool:
        """
        Whether we can use the fastpaths implement in _libs.join
        """
        # Note: this will need to be updated when e.g. Nullable dtypes
        #  are supported in Indexes.
        return not is_interval_dtype(self.dtype)
