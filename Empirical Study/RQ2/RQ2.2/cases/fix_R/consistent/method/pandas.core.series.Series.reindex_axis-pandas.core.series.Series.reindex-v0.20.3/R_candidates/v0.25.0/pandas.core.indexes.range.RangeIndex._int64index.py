    @cache_readonly
    def _int64index(self):
        return Int64Index._simple_new(self._data, name=self.name)
