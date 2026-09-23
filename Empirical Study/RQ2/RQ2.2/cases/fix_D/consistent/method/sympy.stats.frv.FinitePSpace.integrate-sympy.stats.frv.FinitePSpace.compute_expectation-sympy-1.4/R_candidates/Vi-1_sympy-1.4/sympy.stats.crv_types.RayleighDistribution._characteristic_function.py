    def _characteristic_function(self, t):
        sigma = self.sigma
        return 1 - sigma*t*exp(-sigma**2*t**2/2) * sqrt(pi/2) * (erfi(sigma*t/sqrt(2)) - I)
