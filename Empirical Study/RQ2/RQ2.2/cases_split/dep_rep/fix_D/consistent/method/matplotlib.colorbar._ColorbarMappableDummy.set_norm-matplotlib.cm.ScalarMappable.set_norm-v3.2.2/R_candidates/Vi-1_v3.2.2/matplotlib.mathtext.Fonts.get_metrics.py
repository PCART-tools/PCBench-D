    def get_metrics(self, font, font_class, sym, fontsize, dpi, math=True):
        r"""
        *font*: one of the TeX font names::

          tt, it, rm, cal, sf, bf or default/regular (non-math)

        *font_class*: TODO

        *sym*:  a symbol in raw TeX form. e.g., '1', 'x' or '\sigma'

        *fontsize*: font size in points

        *dpi*: current dots-per-inch

        *math*: whether sym is a math character

        Returns an object with the following attributes:

          - *advance*: The advance distance (in points) of the glyph.

          - *height*: The height of the glyph in points.

          - *width*: The width of the glyph in points.

          - *xmin*, *xmax*, *ymin*, *ymax* - the ink rectangle of the glyph

          - *iceberg* - the distance from the baseline to the top of
            the glyph.  This corresponds to TeX's definition of
            "height".
        """
        info = self._get_info(font, font_class, sym, fontsize, dpi, math)
        return info.metrics
