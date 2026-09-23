    @cache_readonly
    def left(self) -> Index:
        return Index(self._data.left, copy=False)
