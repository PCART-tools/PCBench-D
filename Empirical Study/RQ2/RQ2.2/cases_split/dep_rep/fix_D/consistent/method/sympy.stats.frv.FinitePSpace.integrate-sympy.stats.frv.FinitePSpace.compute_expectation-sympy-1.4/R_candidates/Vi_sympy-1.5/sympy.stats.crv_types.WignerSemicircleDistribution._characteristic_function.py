    def _characteristic_function(self, t):
        return Piecewise((2 * besselj(1, self.R*t) / (self.R*t), Ne(t, 0)),
                         (S.One, True))
