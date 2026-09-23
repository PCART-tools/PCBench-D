    def __call__(self, s):
        if self.is_missing(s):
            return self.missingval
        return int(s)
