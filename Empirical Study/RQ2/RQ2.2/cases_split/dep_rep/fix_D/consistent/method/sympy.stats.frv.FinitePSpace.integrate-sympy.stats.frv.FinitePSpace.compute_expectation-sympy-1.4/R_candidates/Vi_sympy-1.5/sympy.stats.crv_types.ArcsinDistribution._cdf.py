    def _cdf(self, x):
        from sympy import asin
        a, b = self.a, self.b
        return Piecewise(
            (S.Zero, x < a),
            (2*asin(sqrt((x - a)/(b - a)))/pi, x <= b),
            (S.One, True))
