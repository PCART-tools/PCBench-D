    def pdf(self, x):
        d1, d2 = self.d1, self.d2
        return (sqrt((d1*x)**d1*d2**d2 / (d1*x+d2)**(d1+d2))
               / (x * beta_fn(d1/2, d2/2)))
