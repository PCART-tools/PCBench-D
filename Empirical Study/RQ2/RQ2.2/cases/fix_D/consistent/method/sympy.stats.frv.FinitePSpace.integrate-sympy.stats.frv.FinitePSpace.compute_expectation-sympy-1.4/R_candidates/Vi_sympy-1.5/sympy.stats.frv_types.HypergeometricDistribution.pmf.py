    def pmf(self, k):
        N, m, n = self.N, self.m, self.n
        return S(binomial(m, k) * binomial(N - m, n - k))/binomial(N, n)
