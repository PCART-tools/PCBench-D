    def parse(self, s, fonts_object, fontsize, dpi):
        """
        Parse expression *s* using the given *fonts_object* for
        output, at the given *fontsize* and *dpi*.

        Returns the parse tree of `Node` instances.
        """
        self._state_stack = [
            ParserState(fonts_object, 'default', 'rm', fontsize, dpi)]
        self._em_width_cache = {}
        try:
            result = self._expression.parseString(s)
        except ParseBaseException as err:
            # explain becomes a plain method on pyparsing 3 (err.explain(0)).
            raise ValueError("\n" + ParseException.explain(err, 0)) from None
        self._state_stack = None
        self._in_subscript_or_superscript = False
        # prevent operator spacing from leaking into a new expression
        self._em_width_cache = {}
        self._expression.resetCache()
        return result[0]
