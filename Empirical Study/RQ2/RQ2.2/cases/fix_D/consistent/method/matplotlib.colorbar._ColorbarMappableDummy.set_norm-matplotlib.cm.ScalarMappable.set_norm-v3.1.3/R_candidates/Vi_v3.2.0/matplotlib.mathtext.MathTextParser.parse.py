    @functools.lru_cache(50)
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

        if prop is None:
            prop = FontProperties()

        if self._output == 'ps' and rcParams['ps.useafm']:
            font_output = StandardPsFonts(prop)
        else:
            backend = self._backend_mapping[self._output]()
            fontset = rcParams['mathtext.fontset'].lower()
            fontset_class = cbook._check_getitem(
                self._font_type_mapping, fontset=fontset)
            font_output = fontset_class(prop, backend)

        fontsize = prop.get_size_in_points()

        # This is a class variable so we don't rebuild the parser
        # with each request.
        if self._parser is None:
            self.__class__._parser = Parser()

        box = self._parser.parse(s, font_output, fontsize, dpi)
        font_output.set_canvas_size(box.width, box.height, box.depth)
        return font_output.get_results(box)
