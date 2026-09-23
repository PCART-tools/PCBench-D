    @cache_readonly
    def _int64index(self):
        return Int64Index._simple_new(self.asi8, name=self.name)
