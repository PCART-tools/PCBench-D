    def _cdf(self, x):
        eta, b = self.eta, self.b
        return 1 - exp(eta)*exp(-eta*exp(b*x))
