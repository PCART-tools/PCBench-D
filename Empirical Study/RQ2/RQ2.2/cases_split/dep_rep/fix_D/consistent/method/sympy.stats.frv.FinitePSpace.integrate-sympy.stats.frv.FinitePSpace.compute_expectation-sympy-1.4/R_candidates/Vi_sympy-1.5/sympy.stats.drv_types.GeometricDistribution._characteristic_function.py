    def _characteristic_function(self, t):
        p = self.p
        return p * exp(I*t) / (1 - (1 - p)*exp(I*t))
