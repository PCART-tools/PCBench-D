    @property
    def symbols(self):
        return FiniteSet(sym for sym, val in self.elements)
