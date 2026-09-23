    @property
    def domain(self):
        return ProductDomain(*[space.domain for space in self.spaces])
