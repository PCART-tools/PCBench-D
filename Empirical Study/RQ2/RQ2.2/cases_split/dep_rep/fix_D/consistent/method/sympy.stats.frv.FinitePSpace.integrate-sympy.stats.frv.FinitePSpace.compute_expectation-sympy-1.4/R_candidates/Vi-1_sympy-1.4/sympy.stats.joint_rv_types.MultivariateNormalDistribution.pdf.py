    def pdf(self, *args):
        mu, sigma = self.mu, self.sigma
        k = len(mu)
        args = ImmutableMatrix(args)
        x = args - mu
        return  S(1)/sqrt((2*pi)**(k)*det(sigma))*exp(
            -S(1)/2*x.transpose()*(sigma.inv()*\
                x))[0]
