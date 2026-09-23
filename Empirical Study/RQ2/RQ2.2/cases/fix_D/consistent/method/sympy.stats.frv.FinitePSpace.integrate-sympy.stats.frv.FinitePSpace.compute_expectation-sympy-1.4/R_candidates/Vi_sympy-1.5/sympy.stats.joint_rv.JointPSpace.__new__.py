    def __new__(cls, sym, dist):
        if isinstance(dist, SingleContinuousDistribution):
            return SingleContinuousPSpace(sym, dist)
        if isinstance(dist, SingleDiscreteDistribution):
            return SingleDiscretePSpace(sym, dist)
        if isinstance(sym, string_types):
            sym = Symbol(sym)
        if not isinstance(sym, Symbol):
            raise TypeError("s should have been string or Symbol")
        return Basic.__new__(cls, sym, dist)
