    def pdf(self, x):
        b, eta = self.b, self.eta
        return b*exp(-b*x)*exp(-eta*exp(-b*x))*(1+eta*(1-exp(-b*x)))
