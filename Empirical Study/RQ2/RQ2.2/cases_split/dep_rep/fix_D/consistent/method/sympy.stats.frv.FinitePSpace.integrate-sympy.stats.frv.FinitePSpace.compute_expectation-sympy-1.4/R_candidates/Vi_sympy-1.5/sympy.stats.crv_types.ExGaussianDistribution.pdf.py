    def pdf(self, x):
        mean, std, rate = self.mean, self.std, self.rate
        term1 = rate/2
        term2 = exp(rate * (2 * mean + rate * std**2 - 2*x)/2)
        term3 = erfc((mean + rate*std**2 - x)/(sqrt(2)*std))
        return term1*term2*term3
