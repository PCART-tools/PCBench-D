    def pdf(self, x):
        beta, mu = self.beta, self.mu
        z = (x - mu)/beta
        f_max = (1/beta)*exp(-z - exp(-z))
        f_min = (1/beta)*exp(z - exp(z))
        return Piecewise((f_min, self.minimum), (f_max, not self.minimum))
