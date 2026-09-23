    def compute_expectation(self, expr, rvs=None, evaluate=False, **kwargs):
        rvs = rvs or (self.value,)
        if self.value not in rvs:
            return expr

        expr = expr.xreplace(dict((rv, rv.symbol) for rv in rvs))

        x = self.value.symbol
        try:
            return self.distribution.expectation(expr, x, evaluate=evaluate, **kwargs)
        except Exception:
            return Integral(expr * self.pdf, (x, self.set), **kwargs)
