    def _quantile(self, p):
        return self.mu - self.s*log(-S.One + S.One/p)
