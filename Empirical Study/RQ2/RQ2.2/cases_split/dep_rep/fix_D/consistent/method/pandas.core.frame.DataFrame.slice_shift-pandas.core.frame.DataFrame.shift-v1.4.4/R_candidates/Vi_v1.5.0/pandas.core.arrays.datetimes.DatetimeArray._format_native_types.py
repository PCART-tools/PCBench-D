    def _format_native_types(
        self, *, na_rep="NaT", date_format=None, **kwargs
    ) -> npt.NDArray[np.object_]:
        from pandas.io.formats.format import get_format_datetime64_from_values

        fmt = get_format_datetime64_from_values(self, date_format)

        return tslib.format_array_from_datetime(
            self.asi8, tz=self.tz, format=fmt, na_rep=na_rep, reso=self._reso
        )
