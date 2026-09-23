    def font(self, s, loc, toks):
        name, = toks
        self.get_state().font = name
        return []
