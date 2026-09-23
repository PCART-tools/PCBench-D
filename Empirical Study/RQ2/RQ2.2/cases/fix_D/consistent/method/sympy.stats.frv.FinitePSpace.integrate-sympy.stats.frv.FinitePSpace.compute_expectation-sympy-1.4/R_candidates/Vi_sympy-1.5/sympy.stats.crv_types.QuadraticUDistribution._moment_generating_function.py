    def _moment_generating_function(self, t):
        a, b = self.a, self.b

        return -3 * (exp(a*t) * (4  + (a**2 + 2*a*(-2 + b) + b**2) * t) - exp(b*t) * (4 + (-4*b + (a + b)**2) * t)) / ((a-b)**3 * t**2)
