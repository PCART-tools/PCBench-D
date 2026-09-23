    @cache_readonly
    def mid(self) -> Index:
        return Index(self._data.mid, copy=False)
