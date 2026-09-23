    def _format_value(self, val):
        if lib.checknull(val):
            val = self.na_rep
        if self.float_format is not None and com.is_float(val):
            val = float(self.float_format % val)
        return val
