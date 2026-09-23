    @property
    @cacheit
    def dict(self):
        N, m, n = self.N, self.m, self.n
        N, m, n = list(map(sympify, (N, m, n)))
        density = dict((sympify(k),
                        Rational(binomial(m, k) * binomial(N - m, n - k),
                                 binomial(N, n)))
                        for k in range(max(0, n + m - N), min(m, n) + 1))
        return density
