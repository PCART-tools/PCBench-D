    def compute_density(self, expr):
        if self._is_symbolic:
            rv = list(random_symbols(expr))[0]
            k = Dummy('k', integer=True)
            cond = True if not isinstance(expr, (Relational, Logic)) \
                     else expr.subs(rv, k)
            return Lambda(k,
            Piecewise((self.pmf(k), And(k >= self.args[1].low,
            k <= self.args[1].high, cond)), (S.Zero, True)))
        expr = rv_subs(expr, self.values)
        return FinitePSpace(self.domain, self.distribution).compute_density(expr)
