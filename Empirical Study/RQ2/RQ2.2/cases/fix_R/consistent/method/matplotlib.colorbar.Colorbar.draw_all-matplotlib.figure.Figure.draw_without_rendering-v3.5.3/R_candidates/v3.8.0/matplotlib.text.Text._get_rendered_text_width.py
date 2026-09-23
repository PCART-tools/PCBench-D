    def _get_rendered_text_width(self, text):
        """
        Return the width of a given text string, in pixels.
        """

        w, h, d = self._renderer.get_text_width_height_descent(
            text,
            self.get_fontproperties(),
            cbook.is_math_text(text))
        return math.ceil(w)
