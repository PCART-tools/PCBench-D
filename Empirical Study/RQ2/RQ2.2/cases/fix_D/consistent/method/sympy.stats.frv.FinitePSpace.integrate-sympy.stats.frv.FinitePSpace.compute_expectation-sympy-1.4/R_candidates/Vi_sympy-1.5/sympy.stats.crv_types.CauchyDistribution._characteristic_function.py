    def _characteristic_function(self, t):
        return exp(self.x0 * I * t -  self.gamma * Abs(t))
