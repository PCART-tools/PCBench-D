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
