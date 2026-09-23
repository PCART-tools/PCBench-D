    @cache_readonly
    def _int64index(self):
        return Int64Index(self._data, name=self.name, fastpath=True)
