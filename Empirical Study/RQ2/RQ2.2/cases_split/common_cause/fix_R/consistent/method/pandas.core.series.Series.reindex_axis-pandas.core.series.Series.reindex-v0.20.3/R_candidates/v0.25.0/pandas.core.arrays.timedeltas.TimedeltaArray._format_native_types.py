    def _format_native_types(self, na_rep="NaT", date_format=None):
        from pandas.io.formats.format import _get_format_timedelta64

        formatter = _get_format_timedelta64(self._data, na_rep)
        return np.array([formatter(x) for x in self._data])
