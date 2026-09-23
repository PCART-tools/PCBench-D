class TruetypeFonts(Fonts):
    """
    A generic base class for all font setups that use Truetype fonts
    (through FT2Font).
    """
    def __init__(self, default_font_prop, mathtext_backend):
        super().__init__(default_font_prop, mathtext_backend)
        self.glyphd = {}
        self._fonts = {}

        filename = findfont(default_font_prop)
        default_font = get_font(filename)
        self._fonts['default'] = default_font
        self._fonts['regular'] = default_font

    @_api.deprecated("3.4")
    def destroy(self):
        self.glyphd = None
        super().destroy()

    def _get_font(self, font):
        if font in self.fontmap:
            basename = self.fontmap[font]
        else:
            basename = font
        cached_font = self._fonts.get(basename)
        if cached_font is None and os.path.exists(basename):
            cached_font = get_font(basename)
            self._fonts[basename] = cached_font
            self._fonts[cached_font.postscript_name] = cached_font
            self._fonts[cached_font.postscript_name.lower()] = cached_font
        return cached_font

    def _get_offset(self, font, glyph, fontsize, dpi):
        if font.postscript_name == 'Cmex10':
            return (glyph.height / 64 / 2) + (fontsize/3 * dpi/72)
        return 0.

    def _get_info(self, fontname, font_class, sym, fontsize, dpi, math=True):
        key = fontname, font_class, sym, fontsize, dpi
        bunch = self.glyphd.get(key)
        if bunch is not None:
            return bunch

        font, num, symbol_name, fontsize, slanted = \
            self._get_glyph(fontname, font_class, sym, fontsize, math)

        font.set_size(fontsize, dpi)
        glyph = font.load_char(
            num,
            flags=self.mathtext_backend.get_hinting_type())

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

        result = self.glyphd[key] = types.SimpleNamespace(
            font            = font,
            fontsize        = fontsize,
            postscript_name = font.postscript_name,
            metrics         = metrics,
            symbol_name     = symbol_name,
            num             = num,
            glyph           = glyph,
            offset          = offset
            )
        return result

    def get_xheight(self, fontname, fontsize, dpi):
        font = self._get_font(fontname)
        font.set_size(fontsize, dpi)
        pclt = font.get_sfnt_table('pclt')
        if pclt is None:
            # Some fonts don't store the xHeight, so we do a poor man's xHeight
            metrics = self.get_metrics(
                fontname, mpl.rcParams['mathtext.default'], 'x', fontsize, dpi)
            return metrics.iceberg
        xHeight = (pclt['xHeight'] / 64.0) * (fontsize / 12.0) * (dpi / 100.0)
        return xHeight

    def get_underline_thickness(self, font, fontsize, dpi):
        # This function used to grab underline thickness from the font
        # metrics, but that information is just too un-reliable, so it
        # is now hardcoded.
        return ((0.75 / 12.0) * fontsize * dpi) / 72.0

    def get_kern(self, font1, fontclass1, sym1, fontsize1,
                 font2, fontclass2, sym2, fontsize2, dpi):
        if font1 == font2 and fontsize1 == fontsize2:
            info1 = self._get_info(font1, fontclass1, sym1, fontsize1, dpi)
            info2 = self._get_info(font2, fontclass2, sym2, fontsize2, dpi)
            font = info1.font
            return font.get_kerning(info1.num, info2.num, KERNING_DEFAULT) / 64
        return super().get_kern(font1, fontclass1, sym1, fontsize1,
                                font2, fontclass2, sym2, fontsize2, dpi)
