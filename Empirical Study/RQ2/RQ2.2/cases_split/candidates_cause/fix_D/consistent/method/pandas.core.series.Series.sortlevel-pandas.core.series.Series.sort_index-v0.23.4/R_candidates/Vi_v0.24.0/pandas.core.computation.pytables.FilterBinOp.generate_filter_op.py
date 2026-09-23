    def generate_filter_op(self, invert=False):
        if (self.op == '!=' and not invert) or (self.op == '==' and invert):
            return lambda axis, vals: ~axis.isin(vals)
        else:
            return lambda axis, vals: axis.isin(vals)
