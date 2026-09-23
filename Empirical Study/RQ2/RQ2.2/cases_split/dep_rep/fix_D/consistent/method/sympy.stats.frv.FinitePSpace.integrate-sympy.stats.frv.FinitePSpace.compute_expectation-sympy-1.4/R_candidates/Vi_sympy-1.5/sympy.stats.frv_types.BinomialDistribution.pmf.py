    def pmf(self, x):
        n, p = self.n, self.p
        x = sympify(x)
        if not (x.is_number or x.is_Symbol or isinstance(x, RandomSymbol)):
            raise ValueError("'x' expected as an argument of type 'number' or 'Symbol' or , "
                        "'RandomSymbol' not %s" % (type(x)))
        cond = Ge(x, 0) & Le(x, n) & Contains(x, S.Integers)
        return Piecewise((binomial(n, x) * p**x * (1 - p)**(n - x), cond), (S.Zero, True))
