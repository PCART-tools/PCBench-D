    def required_group(self, s, loc, toks):
        return Hlist(toks.get("group", []))
