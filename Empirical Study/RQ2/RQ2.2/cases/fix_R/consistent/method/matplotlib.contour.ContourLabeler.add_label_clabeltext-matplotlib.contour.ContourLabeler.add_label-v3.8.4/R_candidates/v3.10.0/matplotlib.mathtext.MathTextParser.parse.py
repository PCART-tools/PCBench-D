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
        # lru_cache can't decorate parse() directly because prop is
        # mutable, so we key the cache using an internal copy (see
        # Text._get_text_metrics_with_cache for a similar case); likewise,
        # we need to check the mutable state of the text.antialiased and
        # text.hinting rcParams.
        prop = prop.copy() if prop is not None else None
        antialiased = mpl._val_or_rc(antialiased, 'text.antialiased')
        from matplotlib.backends import backend_agg
        load_glyph_flags = {
            "vector": LoadFlags.NO_HINTING,
            "raster": backend_agg.get_hinting_flag(),
        }[self._output_type]
        return self._parse_cached(s, dpi, prop, antialiased, load_glyph_flags)
