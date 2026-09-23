    @property
    def domain(self):
        rvs = random_symbols(self.distribution)
        if len(rvs) == 0:
            return SingleDomain(self.symbol, self.set)
        return ProductDomain(*[rv.pspace.domain for rv in rvs])
