    def unknown_symbol(self, s, loc, toks):
        c, = toks
        raise ParseFatalException(s, loc, "Unknown symbol: %s" % c)
