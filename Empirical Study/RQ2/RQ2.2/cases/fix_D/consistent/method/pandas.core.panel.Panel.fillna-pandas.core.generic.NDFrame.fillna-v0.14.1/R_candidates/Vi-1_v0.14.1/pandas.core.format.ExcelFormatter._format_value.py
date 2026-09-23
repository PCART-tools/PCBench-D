    def _format_value(self, val):
        if lib.checknull(val):
            val = self.na_rep
        elif com.is_float(val):
            if np.isposinf(val):
                val = '-%s' % self.inf_rep
            elif np.isneginf(val):
                val = self.inf_rep
            elif self.float_format is not None:
                val = float(self.float_format % val)
        return val
