class Text(namedtuple('Text', 'x y font glyph width')):
    """
    A glyph in the dvi file.

    The *x* and *y* attributes directly position the glyph.  The *font*,
    *glyph*, and *width* attributes are kept public for back-compatibility,
    but users wanting to draw the glyph themselves are encouraged to instead
    load the font specified by `font_path` at `font_size`, warp it with the
    effects specified by `font_effects`, and load the glyph specified by
    `glyph_name_or_index`.
    """

    def _get_pdftexmap_entry(self):
        return PsfontsMap(find_tex_file("pdftex.map"))[self.font.texname]

    @property
    def font_path(self):
        """The `~pathlib.Path` to the font for this glyph."""
        psfont = self._get_pdftexmap_entry()
        if psfont.filename is None:
            raise ValueError("No usable font file found for {} ({}); "
                             "the font may lack a Type-1 version"
                             .format(psfont.psname.decode("ascii"),
                                     psfont.texname.decode("ascii")))
        return Path(psfont.filename)

    @property
    def font_size(self):
        """The font size."""
        return self.font.size

    @property
    def font_effects(self):
        """
        The "font effects" dict for this glyph.

        This dict contains the values for this glyph of SlantFont and
        ExtendFont (if any), read off :file:`pdftex.map`.
        """
        return self._get_pdftexmap_entry().effects

    @property
    def glyph_name_or_index(self):
        """
        Either the glyph name or the native charmap glyph index.

        If :file:`pdftex.map` specifies an encoding for this glyph's font, that
        is a mapping of glyph indices to Adobe glyph names; use it to convert
        dvi indices to glyph names.  Callers can then convert glyph names to
        glyph indices (with FT_Get_Name_Index/get_name_index), and load the
        glyph using FT_Load_Glyph/load_glyph.

        If :file:`pdftex.map` specifies no encoding, the indices directly map
        to the font's "native" charmap; glyphs should directly loaded using
        FT_Load_Char/load_char after selecting the native charmap.
        """
        entry = self._get_pdftexmap_entry()
        return (_parse_enc(entry.encoding)[self.glyph]
                if entry.encoding is not None else self.glyph)
