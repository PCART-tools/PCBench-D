    @property
    @cacheit
    def dict(self):
        n, p, succ, fail = self.n, self.p, self.succ, self.fail
        n = as_int(n)
        return dict((k*succ + (n - k)*fail,
                binomial(n, k) * p**k * (1 - p)**(n - k)) for k in range(0, n + 1))
