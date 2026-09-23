    @cache_readonly
    def _int64index(self):
        return Int64Index(self.asi8, name=self.name, fastpath=True)
