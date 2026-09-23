    def parse(self, s, dpi = 72, prop = None):
        """
        Parse the given math expression *s* at the given *dpi*.  If
        *prop* is provided, it is a
        :class:`~matplotlib.font_manager.FontProperties` object
        specifying the "default" font to use in the math expression,
        used for all non-math text.

        The results are cached, so multiple calls to :meth:`parse`
        with the same expression should be fast.
        """
        # There is a bug in Python 3.x where it leaks frame references,
        # and therefore can't handle this caching
        if prop is None:
            prop = FontProperties()

        cacheKey = (s, dpi, hash(prop))
        result = self._cache.get(cacheKey)
        if result is not None:
            return result

        if self._output == 'ps' and rcParams['ps.useafm']:
            font_output = StandardPsFonts(prop)
        else:
            backend = self._backend_mapping[self._output]()
            fontset = rcParams['mathtext.fontset']
            fontset_class = self._font_type_mapping.get(fontset.lower())
            if fontset_class is not None:
                font_output = fontset_class(prop, backend)
            else:
                raise ValueError(
                    "mathtext.fontset must be either 'cm', 'dejavuserif', "
                    "'dejavusans', 'stix', 'stixsans', or 'custom'")

        fontsize = prop.get_size_in_points()

        # This is a class variable so we don't rebuild the parser
        # with each request.
        if self._parser is None:
            self.__class__._parser = Parser()

        box = self._parser.parse(s, font_output, fontsize, dpi)
        font_output.set_canvas_size(box.width, box.height, box.depth)
        result = font_output.get_results(box)
        self._cache[cacheKey] = result
        return result
