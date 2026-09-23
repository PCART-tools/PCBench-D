    def pdf(self, x):
        a, b = self.a, self.b
        return b**a/gamma(a) * x**(-a-1) * exp(-b/x)
