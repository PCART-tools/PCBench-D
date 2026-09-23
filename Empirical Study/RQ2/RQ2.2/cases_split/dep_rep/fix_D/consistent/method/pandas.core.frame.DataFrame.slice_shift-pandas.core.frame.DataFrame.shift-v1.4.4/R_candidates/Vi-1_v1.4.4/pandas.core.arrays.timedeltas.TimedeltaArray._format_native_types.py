    @dtl.ravel_compat
    def _format_native_types(
        self, *, na_rep="NaT", date_format=None, **kwargs
    ) -> np.ndarray:
        from pandas.io.formats.format import get_format_timedelta64

        formatter = get_format_timedelta64(self._ndarray, na_rep)
        return np.array([formatter(x) for x in self._ndarray])
