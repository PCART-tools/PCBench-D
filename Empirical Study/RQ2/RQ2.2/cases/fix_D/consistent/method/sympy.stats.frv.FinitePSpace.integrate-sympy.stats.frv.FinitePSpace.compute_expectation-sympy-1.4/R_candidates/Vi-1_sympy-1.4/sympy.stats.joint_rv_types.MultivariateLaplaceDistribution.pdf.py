    def pdf(self, *args):
        from sympy.functions.special.bessel import besselk
        mu, sigma = self.mu, self.sigma
        mu_T = mu.transpose()
        k = S(len(mu))
        sigma_inv = sigma.inv()
        args = ImmutableMatrix(args)
        args_T = args.transpose()
        x = (mu_T*sigma_inv*mu)[0]
        y = (args_T*sigma_inv*args)[0]
        v = 1 - k/2
        return S(2)/((2*pi)**(S(k)/2)*sqrt(det(sigma)))\
        *(y/(2 + x))**(S(v)/2)*besselk(v, sqrt((2 + x)*(y)))\
        *exp((args_T*sigma_inv*mu)[0])
