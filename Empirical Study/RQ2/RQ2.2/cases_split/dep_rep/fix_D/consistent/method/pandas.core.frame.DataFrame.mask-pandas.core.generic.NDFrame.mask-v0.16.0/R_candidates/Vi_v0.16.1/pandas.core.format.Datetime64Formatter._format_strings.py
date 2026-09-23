    def _format_strings(self):

        # we may have a tz, if so, then need to process element-by-element
        # when DatetimeBlockWithTimezones is a reality this could be fixed
        values = self.values
        if not isinstance(values, DatetimeIndex):
            values = DatetimeIndex(values)

        if values.tz is None:
            fmt_values = format_array_from_datetime(values.asi8.ravel(),
                                                    format=_get_format_datetime64_from_values(values, self.date_format),
                                                    na_rep=self.nat_rep).reshape(values.shape)
            fmt_values = fmt_values.tolist()

        else:

            values = values.asobject
            is_dates_only = _is_dates_only(values)
            formatter = (self.formatter or _get_format_datetime64(is_dates_only, values, date_format=self.date_format))
            fmt_values = [ formatter(x) for x in self.values ]

        return fmt_values
