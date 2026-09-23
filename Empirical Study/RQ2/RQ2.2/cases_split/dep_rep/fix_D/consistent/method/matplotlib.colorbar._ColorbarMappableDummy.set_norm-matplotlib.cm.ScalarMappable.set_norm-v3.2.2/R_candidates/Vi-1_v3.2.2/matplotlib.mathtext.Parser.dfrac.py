    def dfrac(self, s, loc, toks):
        assert len(toks) == 1
        assert len(toks[0]) == 2
        state = self.get_state()

        thickness = state.font_output.get_underline_thickness(
            state.font, state.fontsize, state.dpi)
        num, den = toks[0]

        return self._genfrac('', '', thickness,
                             self._math_style_dict['displaystyle'], num, den)
