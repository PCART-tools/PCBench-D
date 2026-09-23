    def _eval_rewrite_as_Probability(self, arg, condition=None, **kwargs):
        rvs = arg.atoms(RandomSymbol)
        if len(rvs) > 1:
            raise NotImplementedError()
        if len(rvs) == 0:
            return arg

        rv = rvs.pop()
        if rv.pspace is None:
            raise ValueError("Probability space not known")

        symbol = rv.symbol
        if symbol.name[0].isupper():
            symbol = Symbol(symbol.name.lower())
        else :
            symbol = Symbol(symbol.name + "_1")

        if rv.pspace.is_Continuous:
            return Integral(arg.replace(rv, symbol)*Probability(Eq(rv, symbol), condition), (symbol, rv.pspace.domain.set.inf, rv.pspace.domain.set.sup))
        else:
            if rv.pspace.is_Finite:
                raise NotImplementedError
            else:
                return Sum(arg.replace(rv, symbol)*Probability(Eq(rv, symbol), condition), (symbol, rv.pspace.domain.set.inf, rv.pspace.set.sup))
