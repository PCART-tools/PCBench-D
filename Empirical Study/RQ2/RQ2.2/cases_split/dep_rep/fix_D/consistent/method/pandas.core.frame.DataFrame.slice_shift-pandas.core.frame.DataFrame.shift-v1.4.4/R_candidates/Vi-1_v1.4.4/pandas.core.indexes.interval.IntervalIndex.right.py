    @cache_readonly
    def right(self) -> Index:
        return Index(self._data.right, copy=False)
