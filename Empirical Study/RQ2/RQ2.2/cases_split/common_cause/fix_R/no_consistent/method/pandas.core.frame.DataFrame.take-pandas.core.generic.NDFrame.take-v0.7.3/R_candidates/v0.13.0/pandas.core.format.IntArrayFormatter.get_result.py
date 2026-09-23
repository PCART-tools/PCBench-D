    def get_result(self):
        if self.formatter:
            formatter = self.formatter
        else:
            formatter = lambda x: '% d' % x

        fmt_values = [formatter(x) for x in self.values]

        return _make_fixed_width(fmt_values, self.justify)
