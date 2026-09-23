    def _cdf(self, x):
        beta, mu = self.beta, self.mu
        return exp(-exp((mu - x)/beta))
