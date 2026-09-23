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
