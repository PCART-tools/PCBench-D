    def pdf(self, x):
        x = sympify(x)
        if x.is_number:
            if x.is_Integer and x >= 1 and x <= self.sides:
                return Rational(1, self.sides)
            return S.Zero
        if x.is_Symbol:
            i = Dummy('i', integer=True, positive=True)
            return Sum(KroneckerDelta(x, i)/self.sides, (i, 1, self.sides))
        raise ValueError("'x' expected as an argument of type 'number' or 'symbol', "
                        "not %s" % (type(x)))
