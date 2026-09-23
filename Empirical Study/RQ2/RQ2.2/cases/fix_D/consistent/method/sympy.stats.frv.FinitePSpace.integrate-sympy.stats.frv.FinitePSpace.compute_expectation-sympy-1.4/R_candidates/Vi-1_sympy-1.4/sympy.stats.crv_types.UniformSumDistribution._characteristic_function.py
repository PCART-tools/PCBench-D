    def _characteristic_function(self, t):
        return ((exp(I*t) - 1) / (I*t))**self.n
