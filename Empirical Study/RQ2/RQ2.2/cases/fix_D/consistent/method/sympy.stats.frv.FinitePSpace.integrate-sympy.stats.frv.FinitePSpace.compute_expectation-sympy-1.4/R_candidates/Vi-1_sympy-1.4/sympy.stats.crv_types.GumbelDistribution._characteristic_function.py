    def _characteristic_function(self, t):
        return gamma(1 - I*self.beta*t) * exp(I*self.mu*t)
