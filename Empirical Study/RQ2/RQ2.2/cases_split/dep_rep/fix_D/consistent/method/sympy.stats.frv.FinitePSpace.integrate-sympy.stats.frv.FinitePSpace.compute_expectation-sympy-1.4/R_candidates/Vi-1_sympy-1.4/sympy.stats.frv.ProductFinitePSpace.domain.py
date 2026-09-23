    @property
    def domain(self):
        return ProductFiniteDomain(*[space.domain for space in self.spaces])
