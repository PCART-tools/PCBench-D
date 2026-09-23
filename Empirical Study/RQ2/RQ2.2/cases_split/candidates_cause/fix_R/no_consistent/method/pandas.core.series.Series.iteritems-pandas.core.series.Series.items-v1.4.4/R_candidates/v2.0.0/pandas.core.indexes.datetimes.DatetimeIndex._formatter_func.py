    @property
    def _formatter_func(self):
        from pandas.io.formats.format import get_format_datetime64

        formatter = get_format_datetime64(is_dates_only_=self._is_dates_only)
        return lambda x: f"'{formatter(x)}'"
