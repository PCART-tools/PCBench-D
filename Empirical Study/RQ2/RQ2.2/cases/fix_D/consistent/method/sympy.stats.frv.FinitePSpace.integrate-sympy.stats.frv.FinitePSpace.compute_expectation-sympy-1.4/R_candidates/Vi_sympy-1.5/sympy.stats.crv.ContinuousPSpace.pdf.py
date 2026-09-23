    @property
    def pdf(self):
        return self.density(*self.domain.symbols)
