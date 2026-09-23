    def get_text_width_height_descent(self, s, prop, ismath):
        if ismath:
            ox, oy, width, height, descent, font_image, used_characters = \
                self.mathtext_parser.parse(s, self.dpi, prop)
            return width, height, descent

        layout, inkRect, logicalRect = self._get_pango_layout(s, prop)
        l, b, w, h = inkRect
        ll, lb, lw, lh = logicalRect

        return w, h + 1, h - lh
