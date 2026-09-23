    def pdf(self, x):
        alpha, beta = self.alpha, self.beta
        return x**(alpha - 1) * (1 - x)**(beta - 1) / beta_fn(alpha, beta)
