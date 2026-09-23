    def genfrac(self, s, loc, toks):
        return self._genfrac(
            toks.get("ldelim", ""), toks.get("rdelim", ""),
            toks["rulesize"], toks.get("style", self._MathStyle.TEXTSTYLE),
            toks["num"], toks["den"])
