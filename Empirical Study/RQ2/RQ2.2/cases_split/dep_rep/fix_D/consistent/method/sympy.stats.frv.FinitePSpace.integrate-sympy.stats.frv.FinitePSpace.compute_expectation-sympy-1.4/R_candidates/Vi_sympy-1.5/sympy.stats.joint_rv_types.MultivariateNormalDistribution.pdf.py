    def pdf(self, *args):
        mu, sigma = self.mu, self.sigma
        k = mu.shape[0]
        args = ImmutableMatrix(args)
        x = args - mu
        return  S.One/sqrt((2*pi)**(k)*det(sigma))*exp(
            Rational(-1, 2)*x.transpose()*(sigma.inv()*\
                x))[0]
