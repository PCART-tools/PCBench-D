    @property
    @cacheit
    def dict(self):
        if self.is_symbolic:
            return Density(self)
        return dict((k, self.pmf(k)) for k in self.set)
