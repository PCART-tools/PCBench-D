    def compute_density(self, expr):
        expr = rv_subs(expr, self.values)
        d = FiniteDensity()
        for elem in self.domain:
            val = expr.xreplace(dict(elem))
            prob = self.prob_of(elem)
            d[val] = d.get(val, S.Zero) + prob
        return d
