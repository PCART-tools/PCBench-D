    def _characteristic_function(self, t):
        return hyper((self.alpha,), (self.alpha + self.beta,), I*t)
