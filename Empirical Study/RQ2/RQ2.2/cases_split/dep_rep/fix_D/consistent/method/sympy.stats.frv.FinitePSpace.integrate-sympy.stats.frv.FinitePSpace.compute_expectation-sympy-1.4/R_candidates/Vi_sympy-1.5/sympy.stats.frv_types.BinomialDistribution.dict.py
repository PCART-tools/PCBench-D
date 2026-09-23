    @property
    @cacheit
    def dict(self):
        if self.is_symbolic:
            return Density(self)
        return dict((k*self.succ + (self.n-k)*self.fail, self.pmf(k))
                    for k in range(0, self.n + 1))
