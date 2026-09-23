    def _quantile(self, p):
        return self.x0 + self.gamma*tan(pi*(p - S.Half))
