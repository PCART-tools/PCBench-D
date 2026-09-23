    def _formatter(self, boxed=False):
        from pandas.io.formats.format import _get_format_timedelta64

        return _get_format_timedelta64(self, box=True)
