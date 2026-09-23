    def _characteristic_function(self, t):
        xm, alpha = self.xm, self.alpha
        return alpha * (-I * xm * t) ** alpha * uppergamma(-alpha, -I * xm * t)
