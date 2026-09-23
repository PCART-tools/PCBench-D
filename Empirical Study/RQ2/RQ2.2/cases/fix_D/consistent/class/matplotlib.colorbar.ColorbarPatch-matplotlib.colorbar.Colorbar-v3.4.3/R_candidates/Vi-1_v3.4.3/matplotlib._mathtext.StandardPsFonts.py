class StandardPsFonts(Fonts):
    """
    Use the standard postscript fonts for rendering to backend_ps

    Unlike the other font classes, BakomaFont and UnicodeFont, this
    one requires the Ps backend.
    """
    basepath = str(cbook._get_data_path('fonts/afm'))

    fontmap = {
        'cal': 'pzcmi8a',  # Zapf Chancery
        'rm':  'pncr8a',   # New Century Schoolbook
        'tt':  'pcrr8a',   # Courier
        'it':  'pncri8a',  # New Century Schoolbook Italic
        'sf':  'phvr8a',   # Helvetica
        'bf':  'pncb8a',   # New Century Schoolbook Bold
        None:  'psyr',     # Symbol
    }

    def __init__(self, default_font_prop, mathtext_backend=None):
        if mathtext_backend is None:
            # Circular import, can be dropped after public access to
            # StandardPsFonts is removed and mathtext_backend made a required
            # parameter.
            from . import mathtext
            mathtext_backend = mathtext.MathtextBackendPath()
        super().__init__(default_font_prop, mathtext_backend)
        self.glyphd = {}
        self.fonts = {}

        filename = findfont(default_font_prop, fontext='afm',
                            directory=self.basepath)
        if filename is None:
            filename = findfont('Helvetica', fontext='afm',
                                directory=self.basepath)
        with open(filename, 'rb') as fd:
            default_font = AFM(fd)
        default_font.fname = filename

        self.fonts['default'] = default_font
        self.fonts['regular'] = default_font

    pswriter = _api.deprecated("3.4")(property(lambda self: StringIO()))

    def _get_font(self, font):
        if font in self.fontmap:
            basename = self.fontmap[font]
        else:
            basename = font

        cached_font = self.fonts.get(basename)
        if cached_font is None:
            fname = os.path.join(self.basepath, basename + ".afm")
            with open(fname, 'rb') as fd:
                cached_font = AFM(fd)
            cached_font.fname = fname
            self.fonts[basename] = cached_font
            self.fonts[cached_font.get_fontname()] = cached_font
        return cached_font

    def _get_info(self, fontname, font_class, sym, fontsize, dpi, math=True):
        """Load the cmfont, metrics and glyph with caching."""
        key = fontname, sym, fontsize, dpi
        tup = self.glyphd.get(key)

        if tup is not None:
            return tup

        # Only characters in the "Letter" class should really be italicized.
        # This class includes greek letters, so we're ok
        if (fontname == 'it' and
                (len(sym) > 1
                 or not unicodedata.category(sym).startswith("L"))):
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
            _log.warning(
                "No TeX to built-in Postscript mapping for {!r}".format(sym))

        slanted = (fontname == 'it')
        font = self._get_font(fontname)

        if found_symbol:
            try:
                symbol_name = font.get_name_char(glyph)
            except KeyError:
                _log.warning(
                    "No glyph in standard Postscript font {!r} for {!r}"
                    .format(font.get_fontname(), sym))
                found_symbol = False

        if not found_symbol:
            glyph = '?'
            num = ord(glyph)
            symbol_name = font.get_name_char(glyph)

        offset = 0

        scale = 0.001 * fontsize

        xmin, ymin, xmax, ymax = [val * scale
                                  for val in font.get_bbox_char(glyph)]
        metrics = types.SimpleNamespace(
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

        self.glyphd[key] = types.SimpleNamespace(
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

    def get_kern(self, font1, fontclass1, sym1, fontsize1,
                 font2, fontclass2, sym2, fontsize2, dpi):
        if font1 == font2 and fontsize1 == fontsize2:
            info1 = self._get_info(font1, fontclass1, sym1, fontsize1, dpi)
            info2 = self._get_info(font2, fontclass2, sym2, fontsize2, dpi)
            font = info1.font
            return (font.get_kern_dist(info1.glyph, info2.glyph)
                    * 0.001 * fontsize1)
        return super().get_kern(font1, fontclass1, sym1, fontsize1,
                                font2, fontclass2, sym2, fontsize2, dpi)

    def get_xheight(self, font, fontsize, dpi):
        font = self._get_font(font)
        return font.get_xheight() * 0.001 * fontsize

    def get_underline_thickness(self, font, fontsize, dpi):
        font = self._get_font(font)
        return font.get_underline_thickness() * 0.001 * fontsize
