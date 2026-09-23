    def _draw_xobject_glyph(self, font, fontsize, glyph_idx, x, y):
        """Draw a multibyte character from a Type 3 font as an XObject."""
        symbol_name = font.get_glyph_name(glyph_idx)
        name = self.file._get_xobject_symbol_name(font.fname, symbol_name)
        self.file.output(
            Op.gsave,
            0.001 * fontsize, 0, 0, 0.001 * fontsize, x, y, Op.concat_matrix,
            Name(name), Op.use_xobject,
            Op.grestore,
        )
