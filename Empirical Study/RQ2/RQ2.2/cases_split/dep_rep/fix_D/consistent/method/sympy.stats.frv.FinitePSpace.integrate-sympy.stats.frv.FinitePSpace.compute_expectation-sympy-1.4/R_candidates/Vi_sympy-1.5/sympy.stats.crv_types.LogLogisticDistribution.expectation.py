    def expectation(self, expr, var, **kwargs):
        a, b = self.args
        return Piecewise((S.NaN, b <= 1), (pi*a/(b*sin(pi/b)), True))
