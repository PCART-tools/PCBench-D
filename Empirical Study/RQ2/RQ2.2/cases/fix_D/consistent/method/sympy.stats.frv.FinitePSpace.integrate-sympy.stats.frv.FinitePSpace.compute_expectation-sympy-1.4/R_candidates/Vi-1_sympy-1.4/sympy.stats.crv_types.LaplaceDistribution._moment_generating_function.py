    def _moment_generating_function(self, t):
        return exp(self.mu*t) / (1 - self.b**2*t**2)
