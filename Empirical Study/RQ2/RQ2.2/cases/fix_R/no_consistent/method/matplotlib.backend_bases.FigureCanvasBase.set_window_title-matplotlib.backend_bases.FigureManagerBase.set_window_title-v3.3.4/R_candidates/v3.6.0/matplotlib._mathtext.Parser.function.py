    def function(self, s, loc, toks):
        hlist = self.operatorname(s, loc, toks)
        hlist.function_name = toks["name"]
        return hlist
