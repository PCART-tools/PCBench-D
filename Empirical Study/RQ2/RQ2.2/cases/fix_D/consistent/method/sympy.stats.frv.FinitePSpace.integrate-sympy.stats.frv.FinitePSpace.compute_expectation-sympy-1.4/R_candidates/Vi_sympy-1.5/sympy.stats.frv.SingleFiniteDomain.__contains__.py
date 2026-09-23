    def __contains__(self, other):
        sym, val = tuple(other)[0]
        return sym == self.symbol and val in self.set
