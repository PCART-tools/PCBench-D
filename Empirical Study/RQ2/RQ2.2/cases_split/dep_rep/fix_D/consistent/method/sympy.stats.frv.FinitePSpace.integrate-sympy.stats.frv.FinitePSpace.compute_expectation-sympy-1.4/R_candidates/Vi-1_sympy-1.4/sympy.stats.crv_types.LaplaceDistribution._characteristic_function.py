    def _characteristic_function(self, t):
        return exp(self.mu*I*t) / (1 + self.b**2*t**2)
