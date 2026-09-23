    def text(self, toks: ParseResults) -> T.Any:
        self.push_state()
        state = self.get_state()
        state.font = 'rm'
        hlist = Hlist([Char(c, state) for c in toks[1]])
        self.pop_state()
        return [hlist]
