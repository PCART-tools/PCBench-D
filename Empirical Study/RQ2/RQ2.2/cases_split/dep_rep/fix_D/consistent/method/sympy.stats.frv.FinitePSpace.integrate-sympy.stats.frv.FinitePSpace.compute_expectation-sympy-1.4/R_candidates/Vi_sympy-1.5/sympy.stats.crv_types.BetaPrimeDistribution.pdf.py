    def pdf(self, x):
        alpha, beta = self.alpha, self.beta
        return x**(alpha - 1)*(1 + x)**(-alpha - beta)/beta_fn(alpha, beta)
