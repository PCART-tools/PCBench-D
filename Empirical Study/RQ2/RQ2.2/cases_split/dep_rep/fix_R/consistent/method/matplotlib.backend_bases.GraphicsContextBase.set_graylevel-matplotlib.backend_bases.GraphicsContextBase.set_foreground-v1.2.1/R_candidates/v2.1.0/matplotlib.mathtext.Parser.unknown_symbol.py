    def unknown_symbol(self, s, loc, toks):
        # print "symbol", toks
        c = toks[0]
        raise ParseFatalException(s, loc, "Unknown symbol: %s" % c)
