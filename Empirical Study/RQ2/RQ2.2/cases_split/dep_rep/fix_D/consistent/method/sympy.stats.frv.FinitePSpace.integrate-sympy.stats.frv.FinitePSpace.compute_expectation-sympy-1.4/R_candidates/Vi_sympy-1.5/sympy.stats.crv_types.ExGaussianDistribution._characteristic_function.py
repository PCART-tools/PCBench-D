    def _characteristic_function(self, t):
        mean, std, rate = self.mean, self.std, self.rate
        term1 = (1 - I*t/rate)**(-1)
        term2 = exp(I*mean*t - std**2*t**2/2)
        return term1 * term2
