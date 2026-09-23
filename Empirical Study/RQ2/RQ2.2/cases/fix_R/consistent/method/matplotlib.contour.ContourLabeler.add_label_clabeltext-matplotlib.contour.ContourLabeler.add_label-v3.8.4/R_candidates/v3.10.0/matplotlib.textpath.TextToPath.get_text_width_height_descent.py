    def get_text_width_height_descent(self, s, prop, ismath):
        fontsize = prop.get_size_in_points()

        if ismath == "TeX":
            return TexManager().get_text_width_height_descent(s, fontsize)

        scale = fontsize / self.FONT_SCALE

        if ismath:
            prop = prop.copy()
            prop.set_size(self.FONT_SCALE)
            width, height, descent, *_ = \
                self.mathtext_parser.parse(s, 72, prop)
            return width * scale, height * scale, descent * scale

        font = self._get_font(prop)
        font.set_text(s, 0.0, flags=LoadFlags.NO_HINTING)
        w, h = font.get_width_height()
        w /= 64.0  # convert from subpixels
        h /= 64.0
        d = font.get_descent()
        d /= 64.0
        return w * scale, h * scale, d * scale
