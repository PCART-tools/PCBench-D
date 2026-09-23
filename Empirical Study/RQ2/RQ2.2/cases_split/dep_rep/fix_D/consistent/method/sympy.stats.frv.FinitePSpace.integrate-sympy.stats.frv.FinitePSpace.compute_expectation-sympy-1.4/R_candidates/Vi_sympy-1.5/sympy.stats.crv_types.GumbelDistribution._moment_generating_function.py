    def _moment_generating_function(self, t):
        mgf_max = gamma(1 - self.beta*t) * exp(self.mu*t)
        mgf_min = gamma(1 + self.beta*t) * exp(self.mu*t)
        return Piecewise((mgf_min, self.minimum), (mgf_max, not self.minimum))
