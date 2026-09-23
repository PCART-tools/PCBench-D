    @cache_readonly
    def mid(self):
        return Index(self._data.mid, copy=False)
