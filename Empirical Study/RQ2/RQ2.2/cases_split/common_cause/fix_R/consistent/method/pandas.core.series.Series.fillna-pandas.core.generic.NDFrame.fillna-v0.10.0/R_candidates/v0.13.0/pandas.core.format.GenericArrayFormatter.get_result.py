    def get_result(self):
        fmt_values = self._format_strings()
        return _make_fixed_width(fmt_values, self.justify)
