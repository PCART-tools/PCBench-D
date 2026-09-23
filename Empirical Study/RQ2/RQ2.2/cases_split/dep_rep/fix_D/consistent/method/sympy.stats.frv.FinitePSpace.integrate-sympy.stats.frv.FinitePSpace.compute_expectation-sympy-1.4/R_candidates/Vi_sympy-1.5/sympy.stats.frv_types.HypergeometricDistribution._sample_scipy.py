    def _sample_scipy(self, size):
        N, m, n = int(self.N), int(self.m), int(self.n)
        return scipy.stats.hypergeom.rvs(M=m, n=n, N=N, size=size)
