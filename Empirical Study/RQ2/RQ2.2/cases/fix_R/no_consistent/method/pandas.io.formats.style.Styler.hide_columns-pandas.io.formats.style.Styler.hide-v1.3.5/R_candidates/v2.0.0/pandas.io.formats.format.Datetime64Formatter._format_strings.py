    def _format_strings(self) -> list[str]:
        """we by definition have DO NOT have a TZ"""
        values = self.values

        if not isinstance(values, DatetimeIndex):
            values = DatetimeIndex(values)

        if self.formatter is not None and callable(self.formatter):
            return [self.formatter(x) for x in values]

        fmt_values = values._data._format_native_types(
            na_rep=self.nat_rep, date_format=self.date_format
        )
        return fmt_values.tolist()
