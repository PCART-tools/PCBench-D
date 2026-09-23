    def _format_strings(self) -> list[str]:
        if self.leading_space is False:
            formatter_str = lambda x: f"{x:d}".format(x=x)
        else:
            formatter_str = lambda x: f"{x: d}".format(x=x)
        formatter = self.formatter or formatter_str
        fmt_values = [formatter(x) for x in self.values]
        return fmt_values
