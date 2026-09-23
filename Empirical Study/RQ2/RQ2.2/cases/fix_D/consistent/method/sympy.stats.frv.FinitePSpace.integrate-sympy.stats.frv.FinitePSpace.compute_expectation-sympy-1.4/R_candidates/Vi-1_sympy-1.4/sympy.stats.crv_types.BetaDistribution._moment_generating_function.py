    def _moment_generating_function(self, t):
        return hyper((self.alpha,), (self.alpha + self.beta,), t)
