    @property
    @cacheit
    def dict(self):
        return dict((k, self.pdf(k)) for k in self.set)
