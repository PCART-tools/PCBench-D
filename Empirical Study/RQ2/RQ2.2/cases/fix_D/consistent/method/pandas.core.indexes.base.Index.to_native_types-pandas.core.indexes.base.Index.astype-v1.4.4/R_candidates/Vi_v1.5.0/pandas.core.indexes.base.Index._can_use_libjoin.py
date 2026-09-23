    @cache_readonly
    def _can_use_libjoin(self) -> bool:
        """
        Whether we can use the fastpaths implement in _libs.join
        """
        if type(self) is Index:
            # excludes EAs
            return isinstance(self.dtype, np.dtype)
        return not is_interval_dtype(self.dtype)
