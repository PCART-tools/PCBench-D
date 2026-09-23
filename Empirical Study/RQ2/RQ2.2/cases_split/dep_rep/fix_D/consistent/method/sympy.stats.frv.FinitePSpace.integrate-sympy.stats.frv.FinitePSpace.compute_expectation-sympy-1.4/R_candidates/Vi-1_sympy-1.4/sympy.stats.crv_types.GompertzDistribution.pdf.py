    def pdf(self, x):
        eta, b = self.eta, self.b
        return b*eta*exp(b*x)*exp(eta)*exp(-eta*exp(b*x))
