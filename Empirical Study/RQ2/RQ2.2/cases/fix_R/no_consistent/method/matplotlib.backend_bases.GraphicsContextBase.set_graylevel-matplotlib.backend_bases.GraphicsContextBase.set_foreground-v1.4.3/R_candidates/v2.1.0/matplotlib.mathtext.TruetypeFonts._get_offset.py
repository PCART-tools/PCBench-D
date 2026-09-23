    def _get_offset(self, font, glyph, fontsize, dpi):
        if font.postscript_name == 'Cmex10':
            return ((glyph.height/64.0/2.0) + (fontsize/3.0 * dpi/72.0))
        return 0.
