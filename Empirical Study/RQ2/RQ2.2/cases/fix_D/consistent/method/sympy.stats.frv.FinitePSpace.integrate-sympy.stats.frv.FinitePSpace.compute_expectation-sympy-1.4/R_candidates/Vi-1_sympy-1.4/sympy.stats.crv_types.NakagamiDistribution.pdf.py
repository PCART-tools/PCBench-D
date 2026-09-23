    def pdf(self, x):
        mu, omega = self.mu, self.omega
        return 2*mu**mu/(gamma(mu)*omega**mu)*x**(2*mu - 1)*exp(-mu/omega*x**2)
