    @property
    def domain(self):
        return SingleFiniteDomain(self.symbol, self.distribution.set)
