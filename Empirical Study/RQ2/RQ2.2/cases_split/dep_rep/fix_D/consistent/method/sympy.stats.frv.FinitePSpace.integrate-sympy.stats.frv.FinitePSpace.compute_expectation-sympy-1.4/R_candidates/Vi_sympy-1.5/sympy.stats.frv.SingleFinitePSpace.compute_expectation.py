    def compute_expectation(self, expr, rvs=None, **kwargs):
        if self._is_symbolic:
            rv = random_symbols(expr)[0]
            k = Dummy('k', integer=True)
            expr = expr.subs(rv, k)
            cond = True if not isinstance(expr, (Relational, Logic)) \
                    else expr
            func = self.pmf(k) * k if cond != True else self.pmf(k) * expr
            return Sum(Piecewise((func, cond), (S.Zero, True)),
                (k, self.distribution.low, self.distribution.high)).doit()
        expr = rv_subs(expr, rvs)
        return FinitePSpace(self.domain, self.distribution).compute_expectation(expr, rvs, **kwargs)
