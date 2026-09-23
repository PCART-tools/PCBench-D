    def __call__(self, x, pos=None):
        s = "%s%s" % (self.format_eng(x), self.unit)
        # Remove the trailing separator when there is neither prefix nor unit
        if len(self.sep) > 0 and s.endswith(self.sep):
            s = s[:-len(self.sep)]
        return self.fix_minus(s)
