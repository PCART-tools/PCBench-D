    def __call__(self, s):
        if self.is_missing(s):
            return self.missingval
        tup = time.strptime(s, self.fmt)
        return datetime.date(*tup[:3])
