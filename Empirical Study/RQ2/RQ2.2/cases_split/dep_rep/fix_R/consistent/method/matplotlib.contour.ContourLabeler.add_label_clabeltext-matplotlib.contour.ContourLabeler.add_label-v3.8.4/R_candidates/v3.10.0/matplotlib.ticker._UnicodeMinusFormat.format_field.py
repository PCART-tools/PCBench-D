    def format_field(self, value, format_spec):
        return Formatter.fix_minus(super().format_field(value, format_spec))
