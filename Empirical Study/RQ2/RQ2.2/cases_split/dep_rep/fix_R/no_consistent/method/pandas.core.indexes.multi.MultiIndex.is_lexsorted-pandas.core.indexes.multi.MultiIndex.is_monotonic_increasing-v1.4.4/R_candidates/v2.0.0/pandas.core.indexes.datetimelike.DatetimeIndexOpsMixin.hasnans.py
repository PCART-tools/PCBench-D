    @cache_readonly
    def hasnans(self) -> bool:
        return self._data._hasna
