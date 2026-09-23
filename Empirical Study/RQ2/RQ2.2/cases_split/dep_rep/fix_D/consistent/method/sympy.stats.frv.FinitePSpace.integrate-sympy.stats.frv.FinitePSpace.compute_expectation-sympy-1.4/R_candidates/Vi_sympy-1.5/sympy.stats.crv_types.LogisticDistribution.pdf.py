    def pdf(self, x):
        mu, s = self.mu, self.s
        return exp(-(x - mu)/s)/(s*(1 + exp(-(x - mu)/s))**2)
