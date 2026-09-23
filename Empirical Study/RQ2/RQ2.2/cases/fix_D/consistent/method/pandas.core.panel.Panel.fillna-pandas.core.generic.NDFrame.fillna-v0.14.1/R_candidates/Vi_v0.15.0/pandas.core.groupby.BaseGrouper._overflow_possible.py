    @cache_readonly
    def _overflow_possible(self):
        return _int64_overflow_possible(self.shape)
