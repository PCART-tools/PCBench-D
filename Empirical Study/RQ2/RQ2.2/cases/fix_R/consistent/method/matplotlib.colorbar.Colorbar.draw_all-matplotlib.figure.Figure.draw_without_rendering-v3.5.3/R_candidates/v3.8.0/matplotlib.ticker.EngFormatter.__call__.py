    def __call__(self, x, pos=None):
        s = f"{self.format_eng(x)}{self.unit}"
        # Remove the trailing separator when there is neither prefix nor unit
        if self.sep and s.endswith(self.sep):
            s = s[:-len(self.sep)]
        return self.fix_minus(s)
