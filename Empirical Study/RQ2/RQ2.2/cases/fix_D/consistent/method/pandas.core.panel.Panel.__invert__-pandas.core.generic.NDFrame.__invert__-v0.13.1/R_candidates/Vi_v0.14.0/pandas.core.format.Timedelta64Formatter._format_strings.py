    def _format_strings(self):
        formatter = self.formatter or _get_format_timedelta64(self.values)

        fmt_values = [formatter(x) for x in self.values]

        return fmt_values
