    def pdf(self, x):
        p, a, b = self.p, self.a, self.b
        return a*p/x*((x/b)**(a*p)/(((x/b)**a + 1)**(p + 1)))
