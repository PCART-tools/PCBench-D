    @property
    def values(self):
        return frozenset(RandomSymbol(sym, self) for sym in self.symbols)
