    def __new__(cls, sym, model=None):
        sym = _symbol_converter(sym)
        return Basic.__new__(cls, sym, model)
