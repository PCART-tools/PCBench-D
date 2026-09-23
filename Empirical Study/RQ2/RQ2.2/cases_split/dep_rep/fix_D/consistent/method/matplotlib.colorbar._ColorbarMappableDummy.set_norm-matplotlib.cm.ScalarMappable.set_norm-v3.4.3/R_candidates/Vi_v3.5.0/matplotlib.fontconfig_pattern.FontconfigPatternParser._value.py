    def _value(self, s, loc, tokens):
        return [value_unescape(r'\1', str(tokens[0]))]
