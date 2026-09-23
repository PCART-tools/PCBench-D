    def _characteristic_function(self, t):
        cf_max = gamma(1 - I*self.beta*t) * exp(I*self.mu*t)
        cf_min = gamma(1 + I*self.beta*t) * exp(I*self.mu*t)
        return Piecewise((cf_min, self.minimum), (cf_max, not self.minimum))
