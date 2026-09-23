    def binom(self, s, loc, toks):
        return self._genfrac(
            "(", ")", 0,
            self._MathStyle.TEXTSTYLE, toks["num"], toks["den"])
