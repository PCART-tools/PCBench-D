    def pdf(self, x):
        xm, alpha = self.xm, self.alpha
        return alpha * xm**alpha / x**(alpha + 1)
