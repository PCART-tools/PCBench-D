    def space(self, s, loc, toks):
        num = self._space_widths[toks["space"]]
        box = self._make_space(num)
        return [box]
