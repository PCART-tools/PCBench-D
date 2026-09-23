    def _quantile(self, p):
        a, b = self.alpha, self.beta
        return a*((p/(1 - p))**(1/b))
