    def style_literal(self, s, loc, toks):
        return self._MathStyle(int(toks["style_literal"]))
