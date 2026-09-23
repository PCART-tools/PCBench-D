    def pdf(self, x):
        mu, alpha, beta = self.mu, self.alpha, self.beta
        num = beta*exp(-(Abs(x - mu)/alpha)**beta)
        den = 2*alpha*gamma(1/beta)
        return num/den
