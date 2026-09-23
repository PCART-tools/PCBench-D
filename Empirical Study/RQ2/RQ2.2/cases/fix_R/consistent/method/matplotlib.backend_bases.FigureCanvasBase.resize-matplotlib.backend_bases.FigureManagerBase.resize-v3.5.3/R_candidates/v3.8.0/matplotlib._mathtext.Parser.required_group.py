    def required_group(self, toks: ParseResults) -> T.Any:
        return Hlist(toks.get("group", []))
