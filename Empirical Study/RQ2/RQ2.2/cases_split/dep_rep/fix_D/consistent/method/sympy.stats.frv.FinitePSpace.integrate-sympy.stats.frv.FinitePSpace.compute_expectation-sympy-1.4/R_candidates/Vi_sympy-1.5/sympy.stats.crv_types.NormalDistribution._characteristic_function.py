    def _characteristic_function(self, t):
        mean, std = self.mean, self.std
        return exp(I*mean*t - std**2*t**2/2)
