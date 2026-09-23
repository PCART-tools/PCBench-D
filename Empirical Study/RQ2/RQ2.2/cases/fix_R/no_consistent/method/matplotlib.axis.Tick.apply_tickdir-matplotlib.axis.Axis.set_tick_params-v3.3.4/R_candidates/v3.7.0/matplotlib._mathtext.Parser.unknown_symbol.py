    def unknown_symbol(self, s, loc, toks):
        raise ParseFatalException(s, loc, f"Unknown symbol: {toks['name']}")
