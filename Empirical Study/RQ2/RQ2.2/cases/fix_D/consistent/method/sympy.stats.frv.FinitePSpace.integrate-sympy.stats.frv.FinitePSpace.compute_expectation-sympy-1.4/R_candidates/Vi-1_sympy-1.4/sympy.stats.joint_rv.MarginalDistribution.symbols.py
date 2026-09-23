    @property
    def symbols(self):
        rvs = self.args[1]
        return set([rv.pspace.symbol for rv in rvs])
