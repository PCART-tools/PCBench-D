    @property
    @cacheit
    def dict(self):
        return dict((k, self.p) for k in self.set)
