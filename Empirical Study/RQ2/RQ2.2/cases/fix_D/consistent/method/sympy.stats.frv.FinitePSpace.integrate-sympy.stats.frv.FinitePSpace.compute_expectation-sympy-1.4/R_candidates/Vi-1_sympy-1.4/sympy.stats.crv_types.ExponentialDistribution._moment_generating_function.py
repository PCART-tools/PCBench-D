    def _moment_generating_function(self, t):
        rate = self.rate
        return rate / (rate - t)
