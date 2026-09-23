    @cache_readonly
    def _engine(self):
        return IntervalTree(self.left, self.right, closed=self.closed)
