    def pdf(self, x):
        mu, b = self.mu, self.b
        return 1/(2*b)*exp(-Abs(x - mu)/b)
