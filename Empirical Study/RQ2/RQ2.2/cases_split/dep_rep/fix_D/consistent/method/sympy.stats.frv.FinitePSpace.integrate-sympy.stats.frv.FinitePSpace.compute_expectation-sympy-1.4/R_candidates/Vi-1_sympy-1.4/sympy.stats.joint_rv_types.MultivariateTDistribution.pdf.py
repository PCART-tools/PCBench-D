    def pdf(self, *args):
        from sympy.functions.special.gamma_functions import gamma
        mu, sigma = self.mu, self.shape_mat
        v = S(self.dof)
        k = S(len(mu))
        sigma_inv = sigma.inv()
        args = ImmutableMatrix(args)
        x = args - mu
        return gamma((k + v)/2)/(gamma(v/2)*(v*pi)**(k/2)*sqrt(det(sigma)))\
        *(1 + 1/v*(x.transpose()*sigma_inv*x)[0])**((-v - k)/2)
