    def font(self, s, loc, toks):
        self.get_state().font = toks["font"]
        return []
