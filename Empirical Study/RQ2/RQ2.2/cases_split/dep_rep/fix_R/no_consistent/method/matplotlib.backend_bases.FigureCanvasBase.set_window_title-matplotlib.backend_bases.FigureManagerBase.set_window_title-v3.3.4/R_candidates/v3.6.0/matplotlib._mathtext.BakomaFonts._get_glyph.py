    def _get_glyph(self, fontname, font_class, sym):
        font = None
        if fontname in self.fontmap and sym in latex_to_bakoma:
            basename, num = latex_to_bakoma[sym]
            slanted = (basename == "cmmi10") or sym in self._slanted_symbols
            font = self._get_font(basename)
        elif len(sym) == 1:
            slanted = (fontname == "it")
            font = self._get_font(fontname)
            if font is not None:
                num = ord(sym)
        if font is not None and font.get_char_index(num) != 0:
            return font, num, slanted
        else:
            return self._stix_fallback._get_glyph(fontname, font_class, sym)
