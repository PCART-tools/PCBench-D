    def pdf(self, *x):
        expr, rvs = self.args[0], self.args[1]
        marginalise_out = [i for i in random_symbols(expr) if i not in rvs]
        if isinstance(expr, CompoundDistribution):
            syms = Dummy('x', real=True)
            expr = expr.args[0].pdf(syms)
        elif isinstance(expr, JointDistribution):
            count = len(expr.domain.args)
            x = Dummy('x', real=True, finite=True)
            syms = tuple(Indexed(x, i) for i in count)
            expr = expr.pdf(syms)
        else:
            syms = tuple(rv.pspace.symbol if isinstance(rv, RandomSymbol) else rv.args[0] for rv in rvs)
        return Lambda(syms, self.compute_pdf(expr, marginalise_out))(*x)
