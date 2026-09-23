    def operatorname(self, s, loc, toks):
        self.push_state()
        state = self.get_state()
        state.font = 'rm'
        # Change the font of Chars, but leave Kerns alone
        for c in toks[0]:
            if isinstance(c, Char):
                c.font = 'rm'
                c._update_metrics()
        self.pop_state()
        return Hlist(toks[0])
