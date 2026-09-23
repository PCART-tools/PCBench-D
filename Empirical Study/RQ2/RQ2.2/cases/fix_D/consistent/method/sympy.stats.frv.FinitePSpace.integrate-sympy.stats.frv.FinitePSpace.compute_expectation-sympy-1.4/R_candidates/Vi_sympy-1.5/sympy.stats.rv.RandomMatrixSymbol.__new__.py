    def __new__(cls, symbol, n, m, pspace=None):
        n, m = _sympify(n), _sympify(m)
        symbol = _symbol_converter(symbol)
        return Basic.__new__(cls, symbol, n, m, pspace)
