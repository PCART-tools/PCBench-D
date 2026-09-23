    def _format_strings(self) -> list[str]:
        """we by definition have a TZ"""
        values = self.values.astype(object)
        ido = is_dates_only(values)
        formatter = self.formatter or get_format_datetime64(
            ido, date_format=self.date_format
        )
        fmt_values = [formatter(x) for x in values]

        return fmt_values
