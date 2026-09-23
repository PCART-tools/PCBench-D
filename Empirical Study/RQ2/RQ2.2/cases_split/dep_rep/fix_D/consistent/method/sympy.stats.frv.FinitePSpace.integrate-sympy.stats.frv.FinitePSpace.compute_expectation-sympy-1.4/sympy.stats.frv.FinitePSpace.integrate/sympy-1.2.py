    def integrate(self, expr, rvs=None):
        rvs = rvs or self.values
        expr = expr.xreplace(dict((rs, rs.symbol) for rs in rvs))
        return sum([expr.xreplace(dict(elem)) * self.prob_of(elem)
                for elem in self.domain])
