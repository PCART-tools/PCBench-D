    @cache_readonly
    def _int64index(self) -> Int64Index:
        return Int64Index._simple_new(self.asi8, name=self.name)
