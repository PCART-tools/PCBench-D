    def pdf(self, x):
        a, b = self.alpha, self.beta
        return ((b/a)*(x/a)**(b - 1))/(1 + (x/a)**b)**2
