    def _cdf(self, x):
        sigma = self.sigma
        return 1 - exp(-(x**2/(2*sigma**2)))
