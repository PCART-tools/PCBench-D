    def _moment_generating_function(self, t):
        eta, b = self.eta, self.b
        return eta * exp(eta) * expint(t/b, eta)
