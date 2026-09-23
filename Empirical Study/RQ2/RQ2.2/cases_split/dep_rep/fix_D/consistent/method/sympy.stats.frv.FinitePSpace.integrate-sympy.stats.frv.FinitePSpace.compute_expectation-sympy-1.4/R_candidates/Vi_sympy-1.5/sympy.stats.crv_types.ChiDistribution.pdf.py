    def pdf(self, x):
        return 2**(1 - self.k/2)*x**(self.k - 1)*exp(-x**2/2)/gamma(self.k/2)
