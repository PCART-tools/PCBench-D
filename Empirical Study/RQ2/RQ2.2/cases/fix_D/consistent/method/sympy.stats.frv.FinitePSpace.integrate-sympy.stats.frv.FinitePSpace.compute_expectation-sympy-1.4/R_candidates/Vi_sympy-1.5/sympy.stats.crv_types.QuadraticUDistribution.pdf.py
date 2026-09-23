    def pdf(self, x):
        a, b = self.a, self.b
        alpha = 12 / (b-a)**3
        beta = (a+b) / 2
        return Piecewise(
                  (alpha * (x-beta)**2, And(a<=x, x<=b)),
                  (S.Zero, True))
