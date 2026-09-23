    def binom(self, s, loc, toks):
        (num, den), = toks
        return self._genfrac('(', ')', 0.0, self._MathStyle.TEXTSTYLE,
                             num, den)
