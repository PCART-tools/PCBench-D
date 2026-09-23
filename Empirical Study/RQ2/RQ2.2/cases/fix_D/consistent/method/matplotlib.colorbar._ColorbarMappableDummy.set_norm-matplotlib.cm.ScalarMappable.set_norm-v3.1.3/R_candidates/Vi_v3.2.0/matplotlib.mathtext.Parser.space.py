    def space(self, s, loc, toks):
        assert len(toks) == 1
        num = self._space_widths[toks[0]]
        box = self._make_space(num)
        return [box]
