    def parse(self, s, dpi=72, prop=None, *, antialiased=None):
        """
        Parse the given math expression *s* at the given *dpi*.  If *prop* is
        provided, it is a `.FontProperties` object specifying the "default"
        font to use in the math expression, used for all non-math text.

        The results are cached, so multiple calls to `parse`
        with the same expression should be fast.

        Depending on the *output* type, this returns either a `VectorParse` or
        a `RasterParse`.
        """
        # lru_cache can't decorate parse() directly because prop
        # is mutable; key the cache using an internal copy (see
        # text._get_text_metrics_with_cache for a similar case).
        prop = prop.copy() if prop is not None else None
        antialiased = mpl._val_or_rc(antialiased, 'text.antialiased')
        return self._parse_cached(s, dpi, prop, antialiased)
