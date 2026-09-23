    def compute_expectation(self, expr, variables=None, **kwargs):
        if variables is None:
            variables = self.symbols
        if not variables:
            return expr
        if frozenset(variables) != frozenset(self.symbols):
            raise ValueError("Values should be equal")
        # assumes only intervals
        return Integral(expr, (self.symbol, self.set), **kwargs)
