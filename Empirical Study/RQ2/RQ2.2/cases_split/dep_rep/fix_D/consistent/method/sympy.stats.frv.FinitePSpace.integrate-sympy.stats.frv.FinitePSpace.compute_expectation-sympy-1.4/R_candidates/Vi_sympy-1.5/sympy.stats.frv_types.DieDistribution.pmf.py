    def pmf(self, x):
        x = sympify(x)
        if not (x.is_number or x.is_Symbol or isinstance(x, RandomSymbol)):
            raise ValueError("'x' expected as an argument of type 'number' or 'Symbol' or , "
                        "'RandomSymbol' not %s" % (type(x)))
        cond = Ge(x, 1) & Le(x, self.sides) & Contains(x, S.Integers)
        return Piecewise((S.One/self.sides, cond), (S.Zero, True))
