class Fonts:
    """
    An abstract base class for a system of fonts to use for mathtext.

    The class must be able to take symbol keys and font file names and
    return the character metrics.  It also delegates to a backend class
    to do the actual drawing.
    """

    def __init__(self, default_font_prop, mathtext_backend):
        """
        Parameters
        ----------
        default_font_prop : `~.font_manager.FontProperties`
            The default non-math font, or the base font for Unicode (generic)
            font rendering.
        mathtext_backend : `MathtextBackend` subclass
            Backend to which rendering is actually delegated.
        """
        self.default_font_prop = default_font_prop
        self.mathtext_backend = mathtext_backend
        self.used_characters = {}

    @_api.deprecated("3.4")
    def destroy(self):
        """
        Fix any cyclical references before the object is about
        to be destroyed.
        """
        self.used_characters = None

    def get_kern(self, font1, fontclass1, sym1, fontsize1,
                 font2, fontclass2, sym2, fontsize2, dpi):
        """
        Get the kerning distance for font between *sym1* and *sym2*.

        See `~.Fonts.get_metrics` for a detailed description of the parameters.
        """
        return 0.

    def get_metrics(self, font, font_class, sym, fontsize, dpi, math=True):
        r"""
        Parameters
        ----------
        font : str
            One of the TeX font names: "tt", "it", "rm", "cal", "sf", "bf",
            "default", "regular", "bb", "frak", "scr".  "default" and "regular"
            are synonyms and use the non-math font.
        font_class : str
            One of the TeX font names (as for *font*), but **not** "bb",
            "frak", or "scr".  This is used to combine two font classes.  The
            only supported combination currently is ``get_metrics("frak", "bf",
            ...)``.
        sym : str
            A symbol in raw TeX form, e.g., "1", "x", or "\sigma".
        fontsize : float
            Font size in points.
        dpi : float
            Rendering dots-per-inch.
        math : bool
            Whether we are currently in math mode or not.

        Returns
        -------
        object

            The returned object has the following attributes (all floats,
            except *slanted*):

            - *advance*: The advance distance (in points) of the glyph.
            - *height*: The height of the glyph in points.
            - *width*: The width of the glyph in points.
            - *xmin*, *xmax*, *ymin*, *ymax*: The ink rectangle of the glyph
            - *iceberg*: The distance from the baseline to the top of the
              glyph.  (This corresponds to TeX's definition of "height".)
            - *slanted*: Whether the glyph should be considered as "slanted"
              (currently used for kerning sub/superscripts).
        """
        info = self._get_info(font, font_class, sym, fontsize, dpi, math)
        return info.metrics

    def set_canvas_size(self, w, h, d):
        """
        Set the size of the buffer used to render the math expression.
        Only really necessary for the bitmap backends.
        """
        self.width, self.height, self.depth = np.ceil([w, h, d])
        self.mathtext_backend.set_canvas_size(
            self.width, self.height, self.depth)

    @_api.rename_parameter("3.4", "facename", "font")
    def render_glyph(self, ox, oy, font, font_class, sym, fontsize, dpi):
        """
        At position (*ox*, *oy*), draw the glyph specified by the remaining
        parameters (see `get_metrics` for their detailed description).
        """
        info = self._get_info(font, font_class, sym, fontsize, dpi)
        self.used_characters.setdefault(info.font.fname, set()).add(info.num)
        self.mathtext_backend.render_glyph(ox, oy, info)

    def render_rect_filled(self, x1, y1, x2, y2):
        """
        Draw a filled rectangle from (*x1*, *y1*) to (*x2*, *y2*).
        """
        self.mathtext_backend.render_rect_filled(x1, y1, x2, y2)

    def get_xheight(self, font, fontsize, dpi):
        """
        Get the xheight for the given *font* and *fontsize*.
        """
        raise NotImplementedError()

    def get_underline_thickness(self, font, fontsize, dpi):
        """
        Get the line thickness that matches the given font.  Used as a
        base unit for drawing lines such as in a fraction or radical.
        """
        raise NotImplementedError()

    def get_used_characters(self):
        """
        Get the set of characters that were used in the math
        expression.  Used by backends that need to subset fonts so
        they know which glyphs to include.
        """
        return self.used_characters

    def get_results(self, box):
        """
        Get the data needed by the backend to render the math
        expression.  The return value is backend-specific.
        """
        result = self.mathtext_backend.get_results(
            box, self.get_used_characters())
        if self.destroy != TruetypeFonts.destroy.__get__(self):
            destroy = _api.deprecate_method_override(
                __class__.destroy, self, since="3.4")
            if destroy:
                destroy()
        return result

    def get_sized_alternatives_for_symbol(self, fontname, sym):
        """
        Override if your font provides multiple sizes of the same
        symbol.  Should return a list of symbols matching *sym* in
        various sizes.  The expression renderer will select the most
        appropriate size for a given situation from this list.
        """
        return [(fontname, sym)]
