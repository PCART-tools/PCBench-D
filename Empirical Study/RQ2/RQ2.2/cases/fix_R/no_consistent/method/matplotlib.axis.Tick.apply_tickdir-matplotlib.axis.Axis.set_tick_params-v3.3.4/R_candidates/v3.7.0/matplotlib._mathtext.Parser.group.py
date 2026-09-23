    def group(self, s, loc, toks):
        grp = Hlist(toks.get("group", []))
        return [grp]
