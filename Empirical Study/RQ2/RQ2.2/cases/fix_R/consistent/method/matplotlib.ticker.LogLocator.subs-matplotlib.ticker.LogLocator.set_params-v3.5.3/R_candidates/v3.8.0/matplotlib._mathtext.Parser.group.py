    def group(self, toks: ParseResults) -> T.Any:
        grp = Hlist(toks.get("group", []))
        return [grp]
