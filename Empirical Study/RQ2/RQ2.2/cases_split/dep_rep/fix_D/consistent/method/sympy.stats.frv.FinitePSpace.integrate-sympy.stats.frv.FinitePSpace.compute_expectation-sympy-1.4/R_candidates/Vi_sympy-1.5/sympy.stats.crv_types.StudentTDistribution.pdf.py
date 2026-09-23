    def pdf(self, x):
        nu = self.nu
        return 1/(sqrt(nu)*beta_fn(S.Half, nu/2))*(1 + x**2/nu)**(-(nu + 1)/2)
