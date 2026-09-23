    @cache_readonly
    def _is_dates_only(self):
        from pandas.io.formats.format import _is_dates_only
        return _is_dates_only(self.values)
