    def font(self, s, loc, toks):
        assert len(toks)==1
        name = toks[0]
        self.get_state().font = name
        return []
