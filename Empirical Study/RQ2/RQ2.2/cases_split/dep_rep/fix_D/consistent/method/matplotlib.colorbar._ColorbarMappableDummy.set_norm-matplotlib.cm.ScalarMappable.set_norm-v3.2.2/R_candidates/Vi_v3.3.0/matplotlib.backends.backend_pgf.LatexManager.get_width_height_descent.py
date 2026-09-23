    def get_width_height_descent(self, text, prop):
        """
        Get the width, total height and descent for a text typeset by the
        current LaTeX environment.
        """

        # apply font properties and define textbox
        prop_cmds = _font_properties_str(prop)
        textbox = "\\sbox0{%s %s}" % (prop_cmds, text)

        # check cache
        if textbox in self.str_cache:
            return self.str_cache[textbox]

        # send textbox to LaTeX and wait for prompt
        self._stdin_writeln(textbox)
        try:
            self._expect_prompt()
        except LatexError as e:
            raise ValueError("Error processing '{}'\nLaTeX Output:\n{}"
                             .format(text, e.latex_output)) from e

        # typeout width, height and text offset of the last textbox
        self._stdin_writeln(r"\typeout{\the\wd0,\the\ht0,\the\dp0}")
        # read answer from latex and advance to the next prompt
        try:
            answer = self._expect_prompt()
        except LatexError as e:
            raise ValueError("Error processing '{}'\nLaTeX Output:\n{}"
                             .format(text, e.latex_output)) from e

        # parse metrics from the answer string
        try:
            width, height, offset = answer.splitlines()[0].split(",")
        except Exception as err:
            raise ValueError("Error processing '{}'\nLaTeX Output:\n{}"
                             .format(text, answer)) from err
        w, h, o = float(width[:-2]), float(height[:-2]), float(offset[:-2])

        # the height returned from LaTeX goes from base to top.
        # the height matplotlib expects goes from bottom to top.
        self.str_cache[textbox] = (w, h + o, o)
        return w, h + o, o
