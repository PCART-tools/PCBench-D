    def stackrel(self, s, loc, toks):
        assert(len(toks) == 1)
        assert(len(toks[0]) == 2)
        num, den = toks[0]

        return self._genfrac('', '', 0.0,
                             self._math_style_dict['textstyle'], num, den)
