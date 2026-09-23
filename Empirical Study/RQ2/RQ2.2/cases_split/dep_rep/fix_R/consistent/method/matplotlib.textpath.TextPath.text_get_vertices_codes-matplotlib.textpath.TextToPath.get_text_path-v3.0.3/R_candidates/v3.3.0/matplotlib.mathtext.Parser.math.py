    def math(self, s, loc, toks):
        hlist = Hlist(toks)
        self.pop_state()
        return [hlist]
