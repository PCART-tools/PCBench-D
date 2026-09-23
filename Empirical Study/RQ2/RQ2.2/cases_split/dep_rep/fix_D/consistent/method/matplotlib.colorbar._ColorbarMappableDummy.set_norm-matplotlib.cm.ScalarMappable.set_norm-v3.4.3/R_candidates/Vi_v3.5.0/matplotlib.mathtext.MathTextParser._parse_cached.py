    @functools.lru_cache(50)
    def _parse_cached(self, s, dpi, prop, force_standard_ps_fonts):
        if prop is None:
            prop = FontProperties()

        fontset_class = (
            _mathtext.StandardPsFonts if force_standard_ps_fonts
            else _api.check_getitem(
                self._font_type_mapping, fontset=prop.get_math_fontfamily()))
        backend = self._backend_mapping[self._output]()
        font_output = fontset_class(prop, backend)

        fontsize = prop.get_size_in_points()

        # This is a class variable so we don't rebuild the parser
        # with each request.
        if self._parser is None:
            self.__class__._parser = _mathtext.Parser()

        box = self._parser.parse(s, font_output, fontsize, dpi)
        font_output.set_canvas_size(box.width, box.height, box.depth)
        return font_output.get_results(box)
