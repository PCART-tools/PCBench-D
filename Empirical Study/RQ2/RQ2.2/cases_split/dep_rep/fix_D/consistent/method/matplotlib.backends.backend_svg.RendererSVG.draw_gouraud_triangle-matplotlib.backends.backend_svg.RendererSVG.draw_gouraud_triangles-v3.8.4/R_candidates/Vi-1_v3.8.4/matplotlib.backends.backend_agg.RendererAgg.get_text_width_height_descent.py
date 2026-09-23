    def get_text_width_height_descent(self, s, prop, ismath):
        # docstring inherited

        _api.check_in_list(["TeX", True, False], ismath=ismath)
        if ismath == "TeX":
            return super().get_text_width_height_descent(s, prop, ismath)

        if ismath:
            ox, oy, width, height, descent, font_image = \
                self.mathtext_parser.parse(s, self.dpi, prop)
            return width, height, descent

        font = self._prepare_font(prop)
        font.set_text(s, 0.0, flags=get_hinting_flag())
        w, h = font.get_width_height()  # width and height of unrotated string
        d = font.get_descent()
        w /= 64.0  # convert from subpixels
        h /= 64.0
        d /= 64.0
        return w, h, d
