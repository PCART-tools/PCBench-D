    def parse(self, s: str, fonts_object: Fonts, fontsize: float, dpi: float) -> Hlist:
        """
        Parse expression *s* using the given *fonts_object* for
        output, at the given *fontsize* and *dpi*.

        Returns the parse tree of `Node` instances.
        """
        self._state_stack = [
            ParserState(fonts_object, 'default', 'rm', fontsize, dpi)]
        self._em_width_cache: dict[tuple[str, float, float], float] = {}
        try:
            result = self._expression.parseString(s)
        except ParseBaseException as err:
            # explain becomes a plain method on pyparsing 3 (err.explain(0)).
            raise ValueError("\n" + ParseException.explain(err, 0)) from None
        self._state_stack = []
        self._in_subscript_or_superscript = False
        # prevent operator spacing from leaking into a new expression
        self._em_width_cache = {}
        ParserElement.resetCache()
        return T.cast(Hlist, result[0])  # Known return type from main.
