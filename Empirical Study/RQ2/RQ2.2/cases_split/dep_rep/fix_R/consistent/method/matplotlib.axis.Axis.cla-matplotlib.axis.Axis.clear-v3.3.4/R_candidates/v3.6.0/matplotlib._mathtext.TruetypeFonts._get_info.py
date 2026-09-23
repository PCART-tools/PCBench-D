    def _get_info(self, fontname, font_class, sym, fontsize, dpi):
        font, num, slanted = self._get_glyph(fontname, font_class, sym)
        font.set_size(fontsize, dpi)
        glyph = font.load_char(num, flags=self.load_glyph_flags)

        xmin, ymin, xmax, ymax = [val/64.0 for val in glyph.bbox]
        offset = self._get_offset(font, glyph, fontsize, dpi)
        metrics = types.SimpleNamespace(
            advance = glyph.linearHoriAdvance/65536.0,
            height  = glyph.height/64.0,
            width   = glyph.width/64.0,
            xmin    = xmin,
            xmax    = xmax,
            ymin    = ymin+offset,
            ymax    = ymax+offset,
            # iceberg is the equivalent of TeX's "height"
            iceberg = glyph.horiBearingY/64.0 + offset,
            slanted = slanted
            )

        return types.SimpleNamespace(
            font            = font,
            fontsize        = fontsize,
            postscript_name = font.postscript_name,
            metrics         = metrics,
            num             = num,
            glyph           = glyph,
            offset          = offset
            )
