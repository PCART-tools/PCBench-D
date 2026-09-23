    @property
    def domain(self):
        rvs = random_symbols(self.distribution)
        if not rvs:
            return SingleDomain(self.symbol, self.distribution.set)
        return ProductDomain(*[rv.pspace.domain for rv in rvs])
