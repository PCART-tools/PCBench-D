    def function(self, s: str, loc: int, toks: ParseResults) -> T.Any:
        hlist = self.operatorname(s, loc, toks)
        hlist.function_name = toks["name"]
        return hlist
