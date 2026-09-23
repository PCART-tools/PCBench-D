    def _characteristic_function(self, t):
        return (1 - self.theta*I*t)**(-self.k)
