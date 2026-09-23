    def _cdf(self, x):
        mu, b = self.mu, self.b
        return Piecewise(
                    (S.Half*exp((x - mu)/b), x < mu),
                    (S.One - S.Half*exp(-(x - mu)/b), x >= mu)
                        )
