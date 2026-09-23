    def _format_strings(self):
        formatter = (self.formatter or
                     _get_format_datetime64_from_values(self.values,
                                                        nat_rep=self.nat_rep,
                                                        date_format=self.date_format))

        fmt_values = [formatter(x) for x in self.values]

        return fmt_values
