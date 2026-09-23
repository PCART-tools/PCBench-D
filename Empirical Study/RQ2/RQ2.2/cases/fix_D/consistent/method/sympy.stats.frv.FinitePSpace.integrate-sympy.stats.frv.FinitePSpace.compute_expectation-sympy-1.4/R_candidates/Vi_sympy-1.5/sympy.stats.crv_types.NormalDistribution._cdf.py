    def _cdf(self, x):
        mean, std = self.mean, self.std
        return erf(sqrt(2)*(-mean + x)/(2*std))/2 + S.Half
