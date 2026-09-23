    @cache_readonly
    def _int64index(self) -> Int64Index:
        return Int64Index._simple_new(self._data, name=self.name)
