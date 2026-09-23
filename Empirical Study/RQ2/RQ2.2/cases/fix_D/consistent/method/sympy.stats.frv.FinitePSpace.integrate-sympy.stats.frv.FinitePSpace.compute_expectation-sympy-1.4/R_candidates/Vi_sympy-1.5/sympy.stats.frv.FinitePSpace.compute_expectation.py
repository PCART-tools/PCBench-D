    def compute_expectation(self, expr, rvs=None, **kwargs):
        rvs = rvs or self.values
        expr = rv_subs(expr, rvs)
        probs = [self.prob_of(elem) for elem in self.domain]
        if isinstance(expr, (Logic, Relational)):
            parse_domain = [tuple(elem)[0][1] for elem in self.domain]
            bools = [expr.xreplace(dict(elem)) for elem in self.domain]
        else:
            parse_domain = [expr.xreplace(dict(elem)) for elem in self.domain]
            bools = [True for elem in self.domain]
        return sum([Piecewise((prob * elem, blv), (S.Zero, True))
                for prob, elem, blv in zip(probs, parse_domain, bools)])
