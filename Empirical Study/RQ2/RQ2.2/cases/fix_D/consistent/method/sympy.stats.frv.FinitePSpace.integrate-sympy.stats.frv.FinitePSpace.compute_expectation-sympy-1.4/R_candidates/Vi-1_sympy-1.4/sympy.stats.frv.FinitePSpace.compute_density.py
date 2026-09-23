    def compute_density(self, expr):
        expr = expr.xreplace(dict(((rs, rs.symbol) for rs in self.values)))
        d = FiniteDensity()
        for elem in self.domain:
            val = expr.xreplace(dict(elem))
            prob = self.prob_of(elem)
            d[val] = d.get(val, 0) + prob
        return d
