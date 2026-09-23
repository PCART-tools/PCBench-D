    def __new__(cls, sym, dim=None):
        sym, dim = _symbol_converter(sym), _sympify(dim)
        if dim.is_integer == False:
            raise ValueError("Dimension of the random matrices must be "
                                "integers, received %s instead."%(dim))
        self = Basic.__new__(cls, sym, dim)
        rmp = RandomMatrixPSpace(sym, model=self)
        return RandomMatrixSymbol(sym, dim, dim, pspace=rmp)
