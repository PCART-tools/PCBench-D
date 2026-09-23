    @staticmethod
    @functools.lru_cache(50)
    def _get_ps_font_and_encoding(texname):
        tex_font_map = dviread.PsfontsMap(dviread.find_tex_file('pdftex.map'))
        font_bunch = tex_font_map[texname]
        if font_bunch.filename is None:
            raise ValueError(
                f"No usable font file found for {font_bunch.psname} "
                f"({texname}). The font may lack a Type-1 version.")

        font = get_font(font_bunch.filename)

        if font_bunch.encoding:
            # If psfonts.map specifies an encoding, use it: it gives us a
            # mapping of glyph indices to Adobe glyph names; use it to convert
            # dvi indices to glyph names and use the FreeType-synthesized
            # unicode charmap to convert glyph names to glyph indices (with
            # FT_Get_Name_Index/get_name_index), and load the glyph using
            # FT_Load_Glyph/load_glyph.  (That charmap has a coverage at least
            # as good as, and possibly better than, the native charmaps.)
            enc = dviread._parse_enc(font_bunch.encoding)
        else:
            # If psfonts.map specifies no encoding, the indices directly
            # map to the font's "native" charmap; so don't use the
            # FreeType-synthesized charmap but the native ones (we can't
            # directly identify it but it's typically an Adobe charmap), and
            # directly load the dvi glyph indices using FT_Load_Char/load_char.
            for charmap_code in [
                    1094992451,  # ADOBE_CUSTOM.
                    1094995778,  # ADOBE_STANDARD.
            ]:
                try:
                    font.select_charmap(charmap_code)
                except (ValueError, RuntimeError):
                    pass
                else:
                    break
            else:
                _log.warning("No supported encoding in font (%s).",
                             font_bunch.filename)
            enc = None

        return font, enc
