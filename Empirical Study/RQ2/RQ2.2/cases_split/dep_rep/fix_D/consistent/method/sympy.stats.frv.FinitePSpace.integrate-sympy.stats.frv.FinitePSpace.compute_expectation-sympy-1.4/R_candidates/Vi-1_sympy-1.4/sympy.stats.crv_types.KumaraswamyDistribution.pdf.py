    def pdf(self, x):
        a, b = self.a, self.b
        return a * b * x**(a-1) * (1-x**a)**(b-1)
