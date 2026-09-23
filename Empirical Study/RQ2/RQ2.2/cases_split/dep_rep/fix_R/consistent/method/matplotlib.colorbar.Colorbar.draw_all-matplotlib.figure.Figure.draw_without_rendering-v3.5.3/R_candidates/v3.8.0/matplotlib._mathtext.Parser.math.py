    def math(self, toks: ParseResults) -> T.Any:
        hlist = Hlist(toks.asList())
        self.pop_state()
        return [hlist]
