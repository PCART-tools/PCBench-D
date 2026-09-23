    def compute_expectation(self, expr, rvs=None, evaluate=False, **kwargs):
        if rvs is None:
            rvs = self.values
        else:
            rvs = frozenset(rvs)

        expr = expr.xreplace(dict((rv, rv.symbol) for rv in rvs))

        domain_symbols = frozenset(rv.symbol for rv in rvs)

        return self.domain.compute_expectation(self.pdf * expr,
                domain_symbols, **kwargs)
