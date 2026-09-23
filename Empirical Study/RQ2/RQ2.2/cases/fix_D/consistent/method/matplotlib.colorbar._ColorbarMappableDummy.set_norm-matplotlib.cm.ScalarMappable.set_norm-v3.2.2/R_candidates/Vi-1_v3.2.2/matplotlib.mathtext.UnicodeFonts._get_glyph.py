    def _get_glyph(self, fontname, font_class, sym, fontsize, math=True):
        found_symbol = False

        if self.use_cmex:
            uniindex = latex_to_cmex.get(sym)
            if uniindex is not None:
                fontname = 'ex'
                found_symbol = True

        if not found_symbol:
            try:
                uniindex = get_unicode_index(sym, math)
                found_symbol = True
            except ValueError:
                uniindex = ord('?')
                _log.warning(
                    "No TeX to unicode mapping for {!a}.".format(sym))

        fontname, uniindex = self._map_virtual_font(
            fontname, font_class, uniindex)

        new_fontname = fontname

        # Only characters in the "Letter" class should be italicized in 'it'
        # mode.  Greek capital letters should be Roman.
        if found_symbol:
            if fontname == 'it' and uniindex < 0x10000:
                char = chr(uniindex)
                if (unicodedata.category(char)[0] != "L"
                        or unicodedata.name(char).startswith("GREEK CAPITAL")):
                    new_fontname = 'rm'

            slanted = (new_fontname == 'it') or sym in self._slanted_symbols
            found_symbol = False
            font = self._get_font(new_fontname)
            if font is not None:
                glyphindex = font.get_char_index(uniindex)
                if glyphindex != 0:
                    found_symbol = True

        if not found_symbol:
            if self.cm_fallback:
                if isinstance(self.cm_fallback, BakomaFonts):
                    _log.warning(
                        "Substituting with a symbol from Computer Modern.")
                if (fontname in ('it', 'regular') and
                        isinstance(self.cm_fallback, StixFonts)):
                    return self.cm_fallback._get_glyph(
                            'rm', font_class, sym, fontsize)
                else:
                    return self.cm_fallback._get_glyph(
                        fontname, font_class, sym, fontsize)
            else:
                if (fontname in ('it', 'regular')
                        and isinstance(self, StixFonts)):
                    return self._get_glyph('rm', font_class, sym, fontsize)
                _log.warning("Font {!r} does not have a glyph for {!a} "
                             "[U+{:x}], substituting with a dummy "
                             "symbol.".format(new_fontname, sym, uniindex))
                fontname = 'rm'
                font = self._get_font(fontname)
                uniindex = 0xA4  # currency char, for lack of anything better
                glyphindex = font.get_char_index(uniindex)
                slanted = False

        symbol_name = font.get_glyph_name(glyphindex)
        return font, uniindex, symbol_name, fontsize, slanted
