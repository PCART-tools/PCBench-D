    def _property(self, s, loc, tokens):
        if len(tokens) == 1:
            if tokens[0] in self._constants:
                key, val = self._constants[tokens[0]]
                self._properties.setdefault(key, []).append(val)
        else:
            key = tokens[0]
            val = tokens[1:]
            self._properties.setdefault(key, []).extend(val)
        return []
