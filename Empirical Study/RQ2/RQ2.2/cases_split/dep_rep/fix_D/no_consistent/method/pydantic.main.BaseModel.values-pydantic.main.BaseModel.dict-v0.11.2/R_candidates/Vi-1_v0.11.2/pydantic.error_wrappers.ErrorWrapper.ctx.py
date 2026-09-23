    @property
    def ctx(self):
        return getattr(self.exc, 'ctx', None)
