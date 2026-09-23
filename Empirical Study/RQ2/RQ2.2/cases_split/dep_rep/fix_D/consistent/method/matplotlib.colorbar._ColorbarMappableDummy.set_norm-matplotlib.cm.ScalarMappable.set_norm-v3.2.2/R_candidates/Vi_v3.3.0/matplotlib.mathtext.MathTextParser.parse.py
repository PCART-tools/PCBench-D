    def parse(self, s, dpi=72, prop=None):
        """
        Parse the given math expression *s* at the given *dpi*.  If *prop* is
        provided, it is a `.FontProperties` object specifying the "default"
        font to use in the math expression, used for all non-math text.

        The results are cached, so multiple calls to `parse`
        with the same expression should be fast.
        """
        # lru_cache can't decorate parse() directly because the ps.useafm and
        # mathtext.fontset rcParams also affect the parse (e.g. by affecting
        # the glyph metrics).
        return self._parse_cached(
            s, dpi, prop, rcParams['ps.useafm'], rcParams['mathtext.fontset'])
