    def _moment_generating_function(self, t):
        mu, s = self.mu, self.s
        return pi**2 * sinh(s*t) * exp(mu*t) /  (s*t*(pi**2 + s**2*t**2))
