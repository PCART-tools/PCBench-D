    def _cdf(self, x):
        p, a, b = self.p, self.a, self.b
        return Piecewise(((S.One + (S(x)/b)**-a)**-p, x>=0),
                    (S.Zero, True))
