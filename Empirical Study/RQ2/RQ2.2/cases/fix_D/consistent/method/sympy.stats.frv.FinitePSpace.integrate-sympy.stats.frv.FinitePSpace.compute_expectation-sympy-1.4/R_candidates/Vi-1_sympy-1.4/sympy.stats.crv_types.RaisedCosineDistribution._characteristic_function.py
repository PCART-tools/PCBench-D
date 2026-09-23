    def _characteristic_function(self, t):
        mu, s = self.mu, self.s
        return Piecewise((exp(-I*pi*mu/s)/2, Eq(t, -pi/s)),
                         (exp(I*pi*mu/s)/2, Eq(t, pi/s)),
                         (pi**2*sin(s*t)*exp(I*mu*t) / (s*t*(pi**2 - s**2*t**2)), True))
