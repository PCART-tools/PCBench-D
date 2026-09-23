    def accent(self, s, loc, toks):
        assert len(toks)==1
        state = self.get_state()
        thickness = state.font_output.get_underline_thickness(
            state.font, state.fontsize, state.dpi)
        if len(toks[0]) != 2:
            raise ParseFatalException("Error parsing accent")
        accent, sym = toks[0]
        if accent in self._wide_accents:
            accent_box = AutoWidthChar(
                '\\' + accent, sym.width, state, char_class=Accent)
        else:
            accent_box = Accent(self._accent_map[accent], state)
        if accent == 'mathring':
            accent_box.shrink()
            accent_box.shrink()
        centered = HCentered([Hbox(sym.width / 4.0), accent_box])
        centered.hpack(sym.width, 'exactly')
        return Vlist([
                centered,
                Vbox(0., thickness * 2.0),
                Hlist([sym])
                ])
