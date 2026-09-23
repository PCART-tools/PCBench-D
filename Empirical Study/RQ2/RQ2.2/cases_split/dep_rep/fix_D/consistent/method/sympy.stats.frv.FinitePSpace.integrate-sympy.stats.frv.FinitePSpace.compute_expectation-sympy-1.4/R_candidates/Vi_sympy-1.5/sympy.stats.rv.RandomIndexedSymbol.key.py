    @property
    def key(self):
        if isinstance(self.symbol, Indexed):
            return self.symbol.args[1]
        elif isinstance(self.symbol, Function):
            return self.symbol.args[0]
