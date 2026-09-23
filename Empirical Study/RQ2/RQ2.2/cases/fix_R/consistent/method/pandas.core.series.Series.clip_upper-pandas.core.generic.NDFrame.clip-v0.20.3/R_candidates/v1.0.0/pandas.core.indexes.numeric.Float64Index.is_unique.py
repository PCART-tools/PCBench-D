    @cache_readonly
    def is_unique(self) -> bool:
        return super().is_unique and self._nan_idxs.size < 2
