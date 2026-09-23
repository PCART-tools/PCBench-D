    @cache_readonly
    def _cached_int64index(self) -> Int64Index:
        return Int64Index._simple_new(self._data, name=self.name)
