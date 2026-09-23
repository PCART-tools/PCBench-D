    def _cdf(self, x):
        a, b = self.alpha, self.beta
        return 1/(1 + (x/a)**(-b))
