    def draw_mathtext(self, gc, x, y, s, prop, angle):
        """Draw mathtext using :mod:`matplotlib.mathtext`."""
        ox, oy, width, height, descent, font_image = \
            self.mathtext_parser.parse(s, self.dpi, prop,
                                       antialiased=gc.get_antialiased())

        xd = descent * sin(radians(angle))
        yd = descent * cos(radians(angle))
        x = round(x + ox + xd)
        y = round(y - oy + yd)
        self._renderer.draw_text_image(font_image, x, y + 1, angle, gc)
