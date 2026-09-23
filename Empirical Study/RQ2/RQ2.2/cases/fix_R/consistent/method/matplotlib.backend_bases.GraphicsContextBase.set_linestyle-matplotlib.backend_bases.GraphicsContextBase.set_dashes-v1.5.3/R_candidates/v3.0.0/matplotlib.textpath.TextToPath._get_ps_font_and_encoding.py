    @staticmethod
    @functools.lru_cache(50)
    def _get_ps_font_and_encoding(texname):
        tex_font_map = dviread.PsfontsMap(dviread.find_tex_file('pdftex.map'))
        font_bunch = tex_font_map[texname]
        if font_bunch.filename is None:
            raise ValueError(
                ("No usable font file found for %s (%s). "
                    "The font may lack a Type-1 version.")
                % (font_bunch.psname, texname))

        font = get_font(font_bunch.filename)

        for charmap_name, charmap_code in [("ADOBE_CUSTOM", 1094992451),
                                           ("ADOBE_STANDARD", 1094995778)]:
            try:
                font.select_charmap(charmap_code)
            except (ValueError, RuntimeError):
                pass
            else:
                break
        else:
            charmap_name = ""
            warnings.warn("No supported encoding in font (%s)." %
                          font_bunch.filename)

        if charmap_name == "ADOBE_STANDARD" and font_bunch.encoding:
            enc0 = dviread.Encoding(font_bunch.encoding)
            enc = {i: _get_adobe_standard_encoding().get(c, None)
                   for i, c in enumerate(enc0.encoding)}
        else:
            enc = {}

        return font, enc
