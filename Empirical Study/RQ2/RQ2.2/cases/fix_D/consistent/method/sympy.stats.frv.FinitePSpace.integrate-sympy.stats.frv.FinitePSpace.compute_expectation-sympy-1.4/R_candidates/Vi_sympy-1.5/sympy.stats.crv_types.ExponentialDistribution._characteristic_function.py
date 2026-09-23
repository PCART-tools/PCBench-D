    def _characteristic_function(self, t):
        rate = self.rate
        return rate / (rate - I*t)
