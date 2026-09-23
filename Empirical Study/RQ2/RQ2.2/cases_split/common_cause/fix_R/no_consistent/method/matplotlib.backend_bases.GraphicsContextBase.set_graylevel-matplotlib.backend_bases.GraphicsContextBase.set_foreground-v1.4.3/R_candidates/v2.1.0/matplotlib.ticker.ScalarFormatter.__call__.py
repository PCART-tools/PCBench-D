    def __call__(self, x, pos=None):
        """
        Return the format for tick value `x` at position `pos`.
        """
        if len(self.locs) == 0:
            return ''
        else:
            s = self.pprint_val(x)
            return self.fix_minus(s)
