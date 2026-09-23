    def pdf(self, x):
        sigma = self.sigma
        return x/sigma**2*exp(-x**2/(2*sigma**2))
