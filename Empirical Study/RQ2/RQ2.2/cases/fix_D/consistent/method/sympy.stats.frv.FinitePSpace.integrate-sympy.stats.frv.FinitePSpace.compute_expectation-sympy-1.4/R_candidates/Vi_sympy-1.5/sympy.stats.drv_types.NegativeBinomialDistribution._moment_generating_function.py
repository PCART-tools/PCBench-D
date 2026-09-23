    def _moment_generating_function(self, t):
        r = self.r
        p = self.p

        return ((1 - p) / (1 - p * exp(t)))**r
