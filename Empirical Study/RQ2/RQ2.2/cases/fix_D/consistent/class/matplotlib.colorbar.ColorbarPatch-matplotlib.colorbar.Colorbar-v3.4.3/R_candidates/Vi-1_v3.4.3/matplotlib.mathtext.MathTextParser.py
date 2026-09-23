class MathTextParser:
    _parser = None

    _backend_mapping = {
        'bitmap': MathtextBackendBitmap,
        'agg':    MathtextBackendAgg,
        'ps':     MathtextBackendPs,
        'pdf':    MathtextBackendPdf,
        'svg':    MathtextBackendSvg,
        'path':   MathtextBackendPath,
        'cairo':  MathtextBackendCairo,
        'macosx': MathtextBackendAgg,
    }
    _font_type_mapping = {
        'cm':          _mathtext.BakomaFonts,
        'dejavuserif': _mathtext.DejaVuSerifFonts,
        'dejavusans':  _mathtext.DejaVuSansFonts,
        'stix':        _mathtext.StixFonts,
        'stixsans':    _mathtext.StixSansFonts,
        'custom':      _mathtext.UnicodeFonts,
    }

    def __init__(self, output):
        """Create a MathTextParser for the given backend *output*."""
        self._output = output.lower()

    def parse(self, s, dpi=72, prop=None, *, _force_standard_ps_fonts=False):
        """
        Parse the given math expression *s* at the given *dpi*.  If *prop* is
        provided, it is a `.FontProperties` object specifying the "default"
        font to use in the math expression, used for all non-math text.

        The results are cached, so multiple calls to `parse`
        with the same expression should be fast.
        """
        if _force_standard_ps_fonts:
            _api.warn_deprecated(
                "3.4",
                removal="3.5",
                message=(
                    "Mathtext using only standard PostScript fonts has "
                    "been likely to produce wrong output for a while, "
                    "has been deprecated in %(since)s and will be removed "
                    "in %(removal)s, after which ps.useafm will have no "
                    "effect on mathtext."
                )
            )

        # lru_cache can't decorate parse() directly because the ps.useafm and
        # mathtext.fontset rcParams also affect the parse (e.g. by affecting
        # the glyph metrics).
        return self._parse_cached(s, dpi, prop, _force_standard_ps_fonts)

    @functools.lru_cache(50)
    def _parse_cached(self, s, dpi, prop, force_standard_ps_fonts):
        if prop is None:
            prop = FontProperties()

        fontset_class = (
            _mathtext.StandardPsFonts if force_standard_ps_fonts
            else _api.check_getitem(
                self._font_type_mapping, fontset=prop.get_math_fontfamily()))
        backend = self._backend_mapping[self._output]()
        font_output = fontset_class(prop, backend)

        fontsize = prop.get_size_in_points()

        # This is a class variable so we don't rebuild the parser
        # with each request.
        if self._parser is None:
            self.__class__._parser = _mathtext.Parser()

        box = self._parser.parse(s, font_output, fontsize, dpi)
        font_output.set_canvas_size(box.width, box.height, box.depth)
        return font_output.get_results(box)

    @_api.deprecated("3.4", alternative="mathtext.math_to_image")
    def to_mask(self, texstr, dpi=120, fontsize=14):
        r"""
        Convert a mathtext string to a grayscale array and depth.

        Parameters
        ----------
        texstr : str
            A valid mathtext string, e.g., r'IQ: $\sigma_i=15$'.
        dpi : float
            The dots-per-inch setting used to render the text.
        fontsize : int
            The font size in points

        Returns
        -------
        array : 2D uint8 alpha
            Mask array of rasterized tex.
        depth : int
            Offset of the baseline from the bottom of the image, in pixels.
        """
        assert self._output == "bitmap"
        prop = FontProperties(size=fontsize)
        ftimage, depth = self.parse(texstr, dpi=dpi, prop=prop)
        return np.asarray(ftimage), depth

    @_api.deprecated("3.4", alternative="mathtext.math_to_image")
    def to_rgba(self, texstr, color='black', dpi=120, fontsize=14):
        r"""
        Convert a mathtext string to an RGBA array and depth.

        Parameters
        ----------
        texstr : str
            A valid mathtext string, e.g., r'IQ: $\sigma_i=15$'.
        color : color
            The text color.
        dpi : float
            The dots-per-inch setting used to render the text.
        fontsize : int
            The font size in points.

        Returns
        -------
        array : (M, N, 4) array
            RGBA color values of rasterized tex, colorized with *color*.
        depth : int
            Offset of the baseline from the bottom of the image, in pixels.
        """
        x, depth = self.to_mask(texstr, dpi=dpi, fontsize=fontsize)

        r, g, b, a = mcolors.to_rgba(color)
        RGBA = np.zeros((x.shape[0], x.shape[1], 4), dtype=np.uint8)
        RGBA[:, :, 0] = 255 * r
        RGBA[:, :, 1] = 255 * g
        RGBA[:, :, 2] = 255 * b
        RGBA[:, :, 3] = x
        return RGBA, depth

    @_api.deprecated("3.4", alternative="mathtext.math_to_image")
    def to_png(self, filename, texstr, color='black', dpi=120, fontsize=14):
        r"""
        Render a tex expression to a PNG file.

        Parameters
        ----------
        filename
            A writable filename or fileobject.
        texstr : str
            A valid mathtext string, e.g., r'IQ: $\sigma_i=15$'.
        color : color
            The text color.
        dpi : float
            The dots-per-inch setting used to render the text.
        fontsize : int
            The font size in points.

        Returns
        -------
        int
            Offset of the baseline from the bottom of the image, in pixels.
        """
        rgba, depth = self.to_rgba(
            texstr, color=color, dpi=dpi, fontsize=fontsize)
        Image.fromarray(rgba).save(filename, format="png")
        return depth

    @_api.deprecated("3.4", alternative="mathtext.math_to_image")
    def get_depth(self, texstr, dpi=120, fontsize=14):
        r"""
        Get the depth of a mathtext string.

        Parameters
        ----------
        texstr : str
            A valid mathtext string, e.g., r'IQ: $\sigma_i=15$'.
        dpi : float
            The dots-per-inch setting used to render the text.

        Returns
        -------
        int
            Offset of the baseline from the bottom of the image, in pixels.
        """
        assert self._output == "bitmap"
        prop = FontProperties(size=fontsize)
        ftimage, depth = self.parse(texstr, dpi=dpi, prop=prop)
        return depth
