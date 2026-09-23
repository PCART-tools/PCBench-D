    def frac(self, s, loc, toks):
        state = self.get_state()
        thickness = state.font_output.get_underline_thickness(
            state.font, state.fontsize, state.dpi)
        (num, den), = toks
        return self._genfrac('', '', thickness, self._MathStyle.TEXTSTYLE,
                             num, den)
