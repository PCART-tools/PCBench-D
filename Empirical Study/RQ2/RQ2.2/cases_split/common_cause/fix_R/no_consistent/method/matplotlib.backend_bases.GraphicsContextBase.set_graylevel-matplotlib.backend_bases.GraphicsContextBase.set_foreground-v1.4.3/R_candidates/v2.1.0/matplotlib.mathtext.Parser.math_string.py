    def math_string(self, s, loc, toks):
        # print "math_string", toks[0][1:-1]
        return self._math_expression.parseString(toks[0][1:-1])
