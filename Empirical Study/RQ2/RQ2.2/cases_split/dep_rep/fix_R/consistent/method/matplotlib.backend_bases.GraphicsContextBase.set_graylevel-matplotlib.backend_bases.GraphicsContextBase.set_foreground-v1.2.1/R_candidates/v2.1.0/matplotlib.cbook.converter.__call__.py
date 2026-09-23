    def __call__(self, s):
        if s == self.missing:
            return self.missingval
        return s
