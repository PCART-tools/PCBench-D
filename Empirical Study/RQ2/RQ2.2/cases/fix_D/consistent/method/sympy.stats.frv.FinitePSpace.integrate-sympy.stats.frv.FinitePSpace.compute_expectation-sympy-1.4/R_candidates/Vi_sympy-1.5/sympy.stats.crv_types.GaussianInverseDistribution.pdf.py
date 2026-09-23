    def pdf(self, x):
        mu, s = self.mean, self.shape
        return exp(-s*(x - mu)**2 / (2*x*mu**2)) * sqrt(s/((2*pi*x**3)))
