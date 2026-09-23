    def _characteristic_function(self, t):
        a, b = self.a, self.b
        return 2 * (-I*b*t)**(a/2) * besselk(sqrt(-4*I*b*t)) / gamma(a)
