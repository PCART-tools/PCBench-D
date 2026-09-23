    def _cdf(self, x):
        return Piecewise(
                (S.One - exp(-self.rate*x), x >= 0),
                (0, True),
        )
