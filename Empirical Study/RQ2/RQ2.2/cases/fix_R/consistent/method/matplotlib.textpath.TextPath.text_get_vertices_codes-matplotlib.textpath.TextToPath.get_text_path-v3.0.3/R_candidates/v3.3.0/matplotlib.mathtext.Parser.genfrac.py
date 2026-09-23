    def genfrac(self, s, loc, toks):
        assert len(toks) == 1
        assert len(toks[0]) == 6

        return self._genfrac(*tuple(toks[0]))
