    @cache_readonly
    def _is_dates_only(self):
        """Return a boolean if we are only dates (and don't have a timezone)"""
        from pandas.io.formats.format import _is_dates_only
        return _is_dates_only(self.values) and self.tz is None
