    def pdf(self, x):
        alpha, beta = self.alpha, self.beta
        return beta * (x/alpha)**(beta - 1) * exp(-(x/alpha)**beta) / alpha
