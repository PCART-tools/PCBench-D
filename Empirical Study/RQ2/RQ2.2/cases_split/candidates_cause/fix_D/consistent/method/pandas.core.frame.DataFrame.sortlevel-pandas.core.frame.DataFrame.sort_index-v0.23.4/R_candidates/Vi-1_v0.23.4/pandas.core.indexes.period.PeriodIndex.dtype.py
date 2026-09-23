    @cache_readonly
    def dtype(self):
        return PeriodDtype.construct_from_string(self.freq)
