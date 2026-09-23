    def pdf(self, x):
        mu, k = self.mu, self.k
        return exp(k*cos(x-mu)) / (2*pi*besseli(0, k))
