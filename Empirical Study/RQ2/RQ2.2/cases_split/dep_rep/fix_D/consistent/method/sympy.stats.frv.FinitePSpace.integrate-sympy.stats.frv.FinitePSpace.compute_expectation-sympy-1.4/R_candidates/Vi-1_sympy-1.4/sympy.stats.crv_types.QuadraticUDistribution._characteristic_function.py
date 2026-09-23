    def _characteristic_function(self, t):
        def _moment_generating_function(self, t):
            a, b = self.a, self.b

            return -3*I*(exp(I*a*t*exp(I*b*t)) * (4*I - (-4*b + (a+b)**2)*t)) / ((a-b)**3 * t**2)
