    def __new__(cls, symbol, set):
        if not isinstance(set, FiniteSet):
            set = FiniteSet(*set)
        return Basic.__new__(cls, symbol, set)
