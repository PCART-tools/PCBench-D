    @property
    def set(self):
        N, m, n = self.N, self.m, self.n
        if self.is_symbolic:
            return Intersection(S.Naturals0, Interval(self.low, self.high))
        return set([i for i in range(max(0, n + m - N), min(n, m) + 1)])
