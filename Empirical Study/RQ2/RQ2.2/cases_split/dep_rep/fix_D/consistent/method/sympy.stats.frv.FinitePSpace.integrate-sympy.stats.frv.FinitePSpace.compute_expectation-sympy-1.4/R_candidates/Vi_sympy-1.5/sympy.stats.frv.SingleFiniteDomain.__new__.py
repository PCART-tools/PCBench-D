    def __new__(cls, symbol, set):
        if not isinstance(set, FiniteSet) and \
            not isinstance(set, Intersection):
            set = FiniteSet(*set)
        return Basic.__new__(cls, symbol, set)
