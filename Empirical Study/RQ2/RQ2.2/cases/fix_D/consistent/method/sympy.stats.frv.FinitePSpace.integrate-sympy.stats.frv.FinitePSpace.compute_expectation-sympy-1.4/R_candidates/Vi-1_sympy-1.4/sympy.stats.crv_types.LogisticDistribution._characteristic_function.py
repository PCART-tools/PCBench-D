    def _characteristic_function(self, t):
        return Piecewise((exp(I*t*self.mu) * pi*self.s*t / sinh(pi*self.s*t), Ne(t, 0)), (S.One, True))
