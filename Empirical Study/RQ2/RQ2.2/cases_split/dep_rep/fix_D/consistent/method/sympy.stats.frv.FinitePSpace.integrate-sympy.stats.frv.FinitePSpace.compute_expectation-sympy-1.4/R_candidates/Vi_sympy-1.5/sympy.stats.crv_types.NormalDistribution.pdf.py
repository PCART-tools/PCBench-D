    def pdf(self, x):
        return exp(-(x - self.mean)**2 / (2*self.std**2)) / (sqrt(2*pi)*self.std)
