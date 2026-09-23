    @property
    def _formatter_func(self):
        from pandas.io.formats.format import _get_format_datetime64

        formatter = _get_format_datetime64(is_dates_only=self._is_dates_only)
        return lambda x: "'%s'" % formatter(x, tz=self.tz)
