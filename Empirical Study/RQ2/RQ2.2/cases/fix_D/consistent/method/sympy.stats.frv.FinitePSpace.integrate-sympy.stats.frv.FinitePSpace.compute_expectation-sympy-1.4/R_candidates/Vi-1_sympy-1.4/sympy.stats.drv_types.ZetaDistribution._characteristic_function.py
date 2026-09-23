    def _characteristic_function(self, t):
        return polylog(self.s, exp(I*t)) / zeta(self.s)
