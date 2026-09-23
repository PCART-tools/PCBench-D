    @cache_readonly
    def _can_use_libjoin(self) -> bool:
        """
        Whether we can use the fastpaths implement in _libs.join
        """
        if type(self) is Index:
            # excludes EAs, but include masks, we get here with monotonic
            # values only, meaning no NA
            return (
                isinstance(self.dtype, np.dtype)
                or isinstance(self.values, BaseMaskedArray)
                or isinstance(self._values, ArrowExtensionArray)
            )
        return not is_interval_dtype(self.dtype)
