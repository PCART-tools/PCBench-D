    def _cdf(self, x):
        a, b = self.a, self.b
        return Piecewise(
            (S.Zero, x < S.Zero),
            (1 - (1 - x**a)**b, x <= S.One),
            (S.One, True))
