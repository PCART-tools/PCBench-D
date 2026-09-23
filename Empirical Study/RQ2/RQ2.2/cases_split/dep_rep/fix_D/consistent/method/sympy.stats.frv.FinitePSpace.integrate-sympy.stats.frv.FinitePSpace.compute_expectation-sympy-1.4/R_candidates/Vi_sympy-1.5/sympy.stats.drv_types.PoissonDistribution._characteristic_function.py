    def _characteristic_function(self, t):
        return exp(self.lamda * (exp(I*t) - 1))
