    def _characteristic_function(self, t):
        a, b, c = self.a, self.b, self.c
        return -2 *((b-c) * exp(I*a*t) - (b-a) * exp(I*c*t) + (c-a) * exp(I*b*t)) / ((b-a)*(c-a)*(b-c)*t**2)
