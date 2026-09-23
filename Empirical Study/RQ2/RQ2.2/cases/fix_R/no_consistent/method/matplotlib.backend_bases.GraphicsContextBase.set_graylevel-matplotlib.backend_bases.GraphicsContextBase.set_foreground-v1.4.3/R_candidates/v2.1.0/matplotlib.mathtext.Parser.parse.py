    def parse(self, s, fonts_object, fontsize, dpi):
        """
        Parse expression *s* using the given *fonts_object* for
        output, at the given *fontsize* and *dpi*.

        Returns the parse tree of :class:`Node` instances.
        """
        self._state_stack = [self.State(fonts_object, 'default', 'rm', fontsize, dpi)]
        self._em_width_cache = {}
        try:
            result = self._expression.parseString(s)
        except ParseBaseException as err:
            raise ValueError("\n".join([
                        "",
                        err.line,
                        " " * (err.column - 1) + "^",
                        six.text_type(err)]))
        self._state_stack = None
        self._em_width_cache = {}
        self._expression.resetCache()
        return result[0]
