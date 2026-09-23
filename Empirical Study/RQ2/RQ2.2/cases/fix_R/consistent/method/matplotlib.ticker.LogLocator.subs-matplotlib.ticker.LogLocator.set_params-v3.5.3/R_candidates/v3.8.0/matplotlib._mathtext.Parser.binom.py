    def binom(self, toks: ParseResults) -> T.Any:
        return self._genfrac(
            "(", ")", 0,
            self._MathStyle.TEXTSTYLE, toks["num"], toks["den"])
