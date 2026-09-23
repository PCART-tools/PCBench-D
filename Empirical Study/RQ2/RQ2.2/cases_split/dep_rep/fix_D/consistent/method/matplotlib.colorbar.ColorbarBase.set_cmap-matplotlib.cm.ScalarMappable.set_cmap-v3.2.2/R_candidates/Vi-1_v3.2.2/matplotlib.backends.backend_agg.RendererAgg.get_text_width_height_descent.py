    def get_text_width_height_descent(self, s, prop, ismath):
        # docstring inherited

        if ismath in ["TeX", "TeX!"]:
            # todo: handle props
            texmanager = self.get_texmanager()
            fontsize = prop.get_size_in_points()
            w, h, d = texmanager.get_text_width_height_descent(
                s, fontsize, renderer=self)
            return w, h, d

        if ismath:
            ox, oy, width, height, descent, fonts, used_characters = \
                self.mathtext_parser.parse(s, self.dpi, prop)
            return width, height, descent

        flags = get_hinting_flag()
        font = self._get_agg_font(prop)
        font.set_text(s, 0.0, flags=flags)
        w, h = font.get_width_height()  # width and height of unrotated string
        d = font.get_descent()
        w /= 64.0  # convert from subpixels
        h /= 64.0
        d /= 64.0
        return w, h, d
