    def style_literal(self, toks: ParseResults) -> T.Any:
        return self._MathStyle(int(toks["style_literal"]))
