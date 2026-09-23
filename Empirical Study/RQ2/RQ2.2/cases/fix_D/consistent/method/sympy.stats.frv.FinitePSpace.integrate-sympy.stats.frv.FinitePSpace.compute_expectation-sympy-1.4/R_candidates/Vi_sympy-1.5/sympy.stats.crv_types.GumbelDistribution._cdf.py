    def _cdf(self, x):
        beta, mu = self.beta, self.mu
        z = (x - mu)/beta
        F_max = exp(-exp(-z))
        F_min = 1 - exp(-exp(z))
        return Piecewise((F_min, self.minimum), (F_max, not self.minimum))
