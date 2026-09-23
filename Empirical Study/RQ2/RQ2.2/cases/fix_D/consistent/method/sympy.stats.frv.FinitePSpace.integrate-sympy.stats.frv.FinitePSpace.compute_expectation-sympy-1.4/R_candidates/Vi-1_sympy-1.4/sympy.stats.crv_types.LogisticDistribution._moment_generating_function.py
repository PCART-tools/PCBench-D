    def _moment_generating_function(self, t):
        return exp(self.mu*t) * Beta(1 - self.s*t, 1 + self.s*t)
