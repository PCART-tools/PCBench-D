    def _get_glyph(self, fontname, font_class, sym, fontsize, math=True):
        symbol_name = None
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

        if font is not None:
            gid = font.get_char_index(num)
            if gid != 0:
                symbol_name = font.get_glyph_name(gid)

        if symbol_name is None:
            return self._stix_fallback._get_glyph(
                fontname, font_class, sym, fontsize, math)

        return font, num, symbol_name, fontsize, slanted
