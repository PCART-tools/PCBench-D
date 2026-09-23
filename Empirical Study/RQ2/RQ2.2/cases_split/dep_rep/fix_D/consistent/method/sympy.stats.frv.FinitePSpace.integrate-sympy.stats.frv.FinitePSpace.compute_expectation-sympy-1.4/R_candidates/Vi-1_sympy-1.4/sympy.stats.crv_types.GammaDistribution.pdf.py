    def pdf(self, x):
        k, theta = self.k, self.theta
        return x**(k - 1) * exp(-x/theta) / (gamma(k)*theta**k)
