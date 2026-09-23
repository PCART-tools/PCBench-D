    def underset(self, s, loc, toks):
        assert len(toks) == 1
        assert len(toks[0]) == 2

        state = self.get_state()
        annotation, body = toks[0]

        return self._genset(state, annotation, body, overunder="under")
