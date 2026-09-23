    def compute_cdf(self, expr):
        if self._is_symbolic:
            d = self.compute_density(expr)
            k = Dummy('k')
            ki = Dummy('ki')
            return Lambda(k, Sum(d(ki), (ki, self.args[1].low, k)))
        expr = rv_subs(expr, self.values)
        return FinitePSpace(self.domain, self.distribution).compute_cdf(expr)
