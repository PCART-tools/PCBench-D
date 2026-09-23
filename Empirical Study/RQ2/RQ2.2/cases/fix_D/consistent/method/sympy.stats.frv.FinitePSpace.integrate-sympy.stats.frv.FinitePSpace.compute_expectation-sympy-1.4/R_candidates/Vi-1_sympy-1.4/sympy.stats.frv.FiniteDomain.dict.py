    @property
    def dict(self):
        return FiniteSet(*[Dict(dict(el)) for el in self.elements])
