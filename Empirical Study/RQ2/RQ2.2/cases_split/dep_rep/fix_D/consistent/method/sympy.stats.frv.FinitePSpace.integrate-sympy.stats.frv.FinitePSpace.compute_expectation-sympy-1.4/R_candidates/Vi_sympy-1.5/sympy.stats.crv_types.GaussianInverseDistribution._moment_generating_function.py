    def _moment_generating_function(self, t):
        mu, s = self.mean, self.shape
        return exp((s/mu)*(1 - sqrt(1 - (2*mu**2*t)/s)))
