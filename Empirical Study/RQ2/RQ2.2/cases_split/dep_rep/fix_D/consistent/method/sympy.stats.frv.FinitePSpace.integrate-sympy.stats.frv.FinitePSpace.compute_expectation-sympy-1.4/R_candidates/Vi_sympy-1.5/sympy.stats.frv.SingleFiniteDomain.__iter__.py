    def __iter__(self):
        return (frozenset(((self.symbol, elem),)) for elem in self.set)
