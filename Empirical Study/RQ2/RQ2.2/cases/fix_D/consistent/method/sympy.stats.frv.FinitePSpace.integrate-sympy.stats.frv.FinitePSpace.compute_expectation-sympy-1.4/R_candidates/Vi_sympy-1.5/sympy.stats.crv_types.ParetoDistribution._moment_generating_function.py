    def _moment_generating_function(self, t):
        xm, alpha = self.xm, self.alpha
        return alpha * (-xm*t)**alpha * uppergamma(-alpha, -xm*t)
