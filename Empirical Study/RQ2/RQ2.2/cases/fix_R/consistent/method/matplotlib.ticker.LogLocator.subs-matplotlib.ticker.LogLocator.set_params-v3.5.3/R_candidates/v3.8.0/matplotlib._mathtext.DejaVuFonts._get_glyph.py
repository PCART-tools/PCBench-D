    def _get_glyph(self, fontname: str, font_class: str,
                   sym: str) -> tuple[FT2Font, int, bool]:
        # Override prime symbol to use Bakoma.
        if sym == r'\prime':
            return self.bakoma._get_glyph(fontname, font_class, sym)
        else:
            # check whether the glyph is available in the display font
            uniindex = get_unicode_index(sym)
            font = self._get_font('ex')
            if font is not None:
                glyphindex = font.get_char_index(uniindex)
                if glyphindex != 0:
                    return super()._get_glyph('ex', font_class, sym)
            # otherwise return regular glyph
            return super()._get_glyph(fontname, font_class, sym)
