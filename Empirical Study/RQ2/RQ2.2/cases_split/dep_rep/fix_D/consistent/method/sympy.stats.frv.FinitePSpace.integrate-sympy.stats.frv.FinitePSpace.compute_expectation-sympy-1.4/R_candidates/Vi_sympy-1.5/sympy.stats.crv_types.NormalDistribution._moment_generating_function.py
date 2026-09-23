    def _moment_generating_function(self, t):
        mean, std = self.mean, self.std
        return exp(mean*t + std**2*t**2/2)
