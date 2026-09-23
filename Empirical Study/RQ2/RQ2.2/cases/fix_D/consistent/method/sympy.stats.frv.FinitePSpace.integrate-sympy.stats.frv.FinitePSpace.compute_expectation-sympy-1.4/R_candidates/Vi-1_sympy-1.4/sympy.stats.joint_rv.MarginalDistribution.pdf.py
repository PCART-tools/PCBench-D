    def pdf(self, *x):
        expr, rvs = self.args[0], self.args[1]
        marginalise_out = [i for i in random_symbols(expr) if i not in self.args[1]]
        syms = [i.pspace.symbol for i in self.args[1]]
        for i in expr.atoms(Indexed):
            if isinstance(i, Indexed) and isinstance(i.base, RandomSymbol)\
             and i not in rvs:
                marginalise_out.append(i)
        if isinstance(expr, CompoundDistribution):
            syms = Dummy('x', real=True)
            expr = expr.args[0].pdf(syms)
        elif isinstance(expr, JointDistribution):
            count = len(expr.domain.args)
            x = Dummy('x', real=True, finite=True)
            syms = [Indexed(x, i) for i in count]
            expr = expression.pdf(syms)
        return Lambda(syms, self.compute_pdf(expr, marginalise_out))(*x)
