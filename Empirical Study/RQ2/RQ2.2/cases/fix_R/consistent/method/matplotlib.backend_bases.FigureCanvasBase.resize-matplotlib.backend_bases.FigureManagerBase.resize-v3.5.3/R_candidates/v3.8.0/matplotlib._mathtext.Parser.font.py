    def font(self, toks: ParseResults) -> T.Any:
        self.get_state().font = toks["font"]
        return []
