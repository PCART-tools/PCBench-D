    def auto_delim(self, s, loc, toks):
        return self._auto_sized_delimiter(
            toks["left"],
            # if "mid" in toks ... can be removed when requiring pyparsing 3.
            toks["mid"].asList() if "mid" in toks else [],
            toks["right"])
