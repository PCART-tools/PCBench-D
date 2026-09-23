    def pdf(self, x):
        a, b, c, d = self.a, self.b, self.c, self.d
        return Piecewise(
            (2*(x-a) / ((b-a)*(d+c-a-b)), And(a <= x, x < b)),
            (2 / (d+c-a-b), And(b <= x, x < c)),
            (2*(d-x) / ((d-c)*(d+c-a-b)), And(c <= x, x <= d)),
            (S.Zero, True))
