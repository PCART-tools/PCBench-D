    def get_result(self):
        if self.formatter:
            formatter = self.formatter
        else:
            formatter = _format_datetime64

        fmt_values = [formatter(x) for x in self.values]
        return _make_fixed_width(fmt_values, self.justify)
