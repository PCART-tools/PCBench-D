    def math_string(self, s, loc, toks):
        return self._math_expression.parseString(toks[0][1:-1])
