    def _format_native_types(self, na_rep='NaT', date_format=None, **kwargs):
        from pandas.io.formats.format import _get_format_datetime64_from_values
        format = _get_format_datetime64_from_values(self, date_format)

        return libts.format_array_from_datetime(self.asi8,
                                                tz=self.tz,
                                                format=format,
                                                na_rep=na_rep)
