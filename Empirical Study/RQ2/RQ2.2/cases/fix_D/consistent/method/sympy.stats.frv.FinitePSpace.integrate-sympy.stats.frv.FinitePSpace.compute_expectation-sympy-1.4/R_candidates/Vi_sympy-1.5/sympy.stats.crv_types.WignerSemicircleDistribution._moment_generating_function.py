    def _moment_generating_function(self, t):
        return Piecewise((2 * besseli(1, self.R*t) / (self.R*t), Ne(t, 0)),
                         (S.One, True))
