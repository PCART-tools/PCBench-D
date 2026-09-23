    def pdf(self, x):
        beta, mu = self.beta, self.mu
        z = (x - mu)/beta
        return (1/beta)*exp(-(z + exp(-z)))
