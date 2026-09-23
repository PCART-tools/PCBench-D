    def pdf(self, k):
        rho = self.rho
        return rho * beta(k, rho + 1)
