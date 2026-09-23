    @property
    def pdf(self):
        p = Mul(*[space.pdf for space in self.spaces])
        return p.subs(dict((rv, rv.symbol) for rv in self.values))
