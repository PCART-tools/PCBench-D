    def _get_info (self, fontname, font_class, sym, fontsize, dpi, math=True):
        'load the cmfont, metrics and glyph with caching'
        key = fontname, sym, fontsize, dpi
        tup = self.glyphd.get(key)

        if tup is not None:
            return tup

        # Only characters in the "Letter" class should really be italicized.
        # This class includes greek letters, so we're ok
        if (fontname == 'it' and
            (len(sym) > 1 or
             not unicodedata.category(six.text_type(sym)).startswith("L"))):
            fontname = 'rm'

        found_symbol = False

        if sym in latex_to_standard:
            fontname, num = latex_to_standard[sym]
            glyph = chr(num)
            found_symbol = True
        elif len(sym) == 1:
            glyph = sym
            num = ord(glyph)
            found_symbol = True
        else:
            warn("No TeX to built-in Postscript mapping for '%s'" % sym,
                 MathTextWarning)

        slanted = (fontname == 'it')
        font = self._get_font(fontname)

        if found_symbol:
            try:
                symbol_name = font.get_name_char(glyph)
            except KeyError:
                warn("No glyph in standard Postscript font '%s' for '%s'" %
                     (font.postscript_name, sym),
                     MathTextWarning)
                found_symbol = False

        if not found_symbol:
            glyph = sym = '?'
            num = ord(glyph)
            symbol_name = font.get_name_char(glyph)

        offset = 0

        scale = 0.001 * fontsize

        xmin, ymin, xmax, ymax = [val * scale
                                  for val in font.get_bbox_char(glyph)]
        metrics = Bunch(
            advance  = font.get_width_char(glyph) * scale,
            width    = font.get_width_char(glyph) * scale,
            height   = font.get_height_char(glyph) * scale,
            xmin = xmin,
            xmax = xmax,
            ymin = ymin+offset,
            ymax = ymax+offset,
            # iceberg is the equivalent of TeX's "height"
            iceberg = ymax + offset,
            slanted = slanted
            )

        self.glyphd[key] = Bunch(
            font            = font,
            fontsize        = fontsize,
            postscript_name = font.get_fontname(),
            metrics         = metrics,
            symbol_name     = symbol_name,
            num             = num,
            glyph           = glyph,
            offset          = offset
            )

        return self.glyphd[key]
