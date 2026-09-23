    @property
    def domain(self):
        return ProductDomain(self.process.index_set,
                             self.process.state_space)
