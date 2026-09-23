    def pdf(self, x):
        a = self.a
        return sqrt(2/pi)*x**2*exp(-x**2/(2*a**2))/a**3
