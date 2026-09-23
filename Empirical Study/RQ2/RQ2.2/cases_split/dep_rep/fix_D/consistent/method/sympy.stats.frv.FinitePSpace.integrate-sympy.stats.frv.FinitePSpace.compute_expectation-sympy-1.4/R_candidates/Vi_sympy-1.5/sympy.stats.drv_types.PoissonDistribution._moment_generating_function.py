    def _moment_generating_function(self, t):
        return exp(self.lamda * (exp(t) - 1))
