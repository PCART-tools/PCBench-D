    def _moment_generating_function(self, t):
        return polylog(self.s, exp(t)) / zeta(self.s)
