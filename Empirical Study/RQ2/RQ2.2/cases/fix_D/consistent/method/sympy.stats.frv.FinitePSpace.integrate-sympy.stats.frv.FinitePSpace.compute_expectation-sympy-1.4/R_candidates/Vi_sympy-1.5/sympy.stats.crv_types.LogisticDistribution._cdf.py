    def _cdf(self, x):
        mu, s = self.mu, self.s
        return S.One/(1 + exp(-(x - mu)/s))
