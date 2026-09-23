    def math_string(self, toks: ParseResults) -> ParseResults:
        return self._math_expression.parseString(toks[0][1:-1], parseAll=True)
