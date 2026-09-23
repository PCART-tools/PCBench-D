    def _format_strings(self):
        formatter = self.formatter or (lambda x: '% d' % x)

        fmt_values = [formatter(x) for x in self.values]

        return fmt_values
