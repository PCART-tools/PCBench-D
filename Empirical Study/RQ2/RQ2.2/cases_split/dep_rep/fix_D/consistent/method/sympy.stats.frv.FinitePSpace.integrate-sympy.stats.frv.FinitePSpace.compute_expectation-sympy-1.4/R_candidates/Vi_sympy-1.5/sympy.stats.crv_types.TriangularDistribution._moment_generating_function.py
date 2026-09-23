    def _moment_generating_function(self, t):
        a, b, c = self.a, self.b, self.c
        return 2 * ((b - c) * exp(a * t) - (b - a) * exp(c * t) + (c - a) * exp(b * t)) / (
        (b - a) * (c - a) * (b - c) * t ** 2)
