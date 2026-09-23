    def pmf(self, x):
        return Piecewise((self.p, x == self.succ),
                         (1 - self.p, x == self.fail),
                         (S.Zero, True))
