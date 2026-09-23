    def compute_expectation(self, expr, rvs=None, evaluate=False, **kwargs):
        syms = tuple(self.value[i] for i in range(self.component_count))
        rvs = rvs or syms
        if not any([i in rvs for i in syms]):
            return expr
        expr = expr*self.pdf
        for rv in rvs:
            if isinstance(rv, Indexed):
                expr = expr.xreplace({rv: Indexed(str(rv.base), rv.args[1])})
            elif isinstance(rv, RandomSymbol):
                expr = expr.xreplace({rv: rv.symbol})
        if self.value in random_symbols(expr):
            raise NotImplementedError(filldedent('''
            Expectations of expression with unindexed joint random symbols
            cannot be calculated yet.'''))
        limits = tuple((Indexed(str(rv.base),rv.args[1]),
            self.distribution.set.args[rv.args[1]]) for rv in syms)
        return Integral(expr, *limits)
