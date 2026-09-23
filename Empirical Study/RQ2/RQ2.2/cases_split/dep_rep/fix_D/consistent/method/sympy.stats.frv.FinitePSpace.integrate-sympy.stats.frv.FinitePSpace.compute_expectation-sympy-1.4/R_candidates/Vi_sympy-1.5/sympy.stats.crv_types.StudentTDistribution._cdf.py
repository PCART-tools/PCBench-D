    def _cdf(self, x):
        nu = self.nu
        return S.Half + x*gamma((nu+1)/2)*hyper((S.Half, (nu+1)/2),
                                (Rational(3, 2),), -x**2/nu)/(sqrt(pi*nu)*gamma(nu/2))
