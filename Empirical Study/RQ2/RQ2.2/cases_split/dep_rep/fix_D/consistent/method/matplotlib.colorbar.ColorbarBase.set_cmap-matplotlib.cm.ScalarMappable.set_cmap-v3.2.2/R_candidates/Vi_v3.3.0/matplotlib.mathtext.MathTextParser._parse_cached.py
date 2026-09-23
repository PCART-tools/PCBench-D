    @functools.lru_cache(50)
    def _parse_cached(self, s, dpi, prop, ps_useafm, fontset):

        if prop is None:
            prop = FontProperties()

        if self._output == 'ps' and ps_useafm:
            font_output = StandardPsFonts(prop)
        else:
            backend = self._backend_mapping[self._output]()
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
