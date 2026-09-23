    def get_text_width_height_descent(self, s, prop, ismath):
        """
        Get the width, height, and descent (offset from the bottom
        to the baseline), in display coords, of the string *s* with
        `.FontProperties` *prop*.
        """
        if ismath == 'TeX':
            # todo: handle props
            texmanager = self._text2path.get_texmanager()
            fontsize = prop.get_size_in_points()
            w, h, d = texmanager.get_text_width_height_descent(
                s, fontsize, renderer=self)
            return w, h, d

        dpi = self.points_to_pixels(72)
        if ismath:
            dims = self._text2path.mathtext_parser.parse(s, dpi, prop)
            return dims[0:3]  # return width, height, descent

        flags = self._text2path._get_hinting_flag()
        font = self._text2path._get_font(prop)
        size = prop.get_size_in_points()
        font.set_size(size, dpi)
        # the width and height of unrotated string
        font.set_text(s, 0.0, flags=flags)
        w, h = font.get_width_height()
        d = font.get_descent()
        w /= 64.0  # convert from subpixels
        h /= 64.0
        d /= 64.0
        return w, h, d
