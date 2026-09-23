    def _moment_generating_function(self, t):
        return gamma(1 - self.beta*t) * exp(I*self.mu*t)
