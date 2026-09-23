    def _format_strings(self):
        formatter = self.formatter or _get_format_timedelta64(self.values, nat_rep=self.nat_rep,
                                                              box=self.box)
        fmt_values = [formatter(x) for x in self.values]
        return fmt_values
