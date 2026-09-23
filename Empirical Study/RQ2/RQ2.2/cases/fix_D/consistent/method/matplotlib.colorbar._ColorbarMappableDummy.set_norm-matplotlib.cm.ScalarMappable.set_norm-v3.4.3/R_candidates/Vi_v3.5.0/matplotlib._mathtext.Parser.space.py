    def space(self, s, loc, toks):
        tok, = toks
        num = self._space_widths[tok]
        box = self._make_space(num)
        return [box]
