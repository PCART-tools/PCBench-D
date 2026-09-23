    def get_text_width_height_descent(self, s, prop, ismath):
        """
        get the width and height in display coords of the string s
        with FontPropertry prop

        """
        if rcParams['text.usetex']:
            texmanager = self.get_texmanager()
            fontsize = prop.get_size_in_points()
            w, h, d = texmanager.get_text_width_height_descent(s, fontsize,
                                                               renderer=self)
            return w, h, d

        if ismath:
            width, height, descent, pswriter, used_characters = \
                self.mathtext_parser.parse(s, 72, prop)
            return width, height, descent

        if rcParams['ps.useafm']:
            if ismath: s = s[1:-1]
            font = self._get_font_afm(prop)
            l,b,w,h,d = font.get_str_bbox_and_descent(s)

            fontsize = prop.get_size_in_points()
            scale = 0.001*fontsize
            w *= scale
            h *= scale
            d *= scale
            return w, h, d

        font = self._get_font_ttf(prop)
        font.set_text(s, 0.0, flags=LOAD_NO_HINTING)
        w, h = font.get_width_height()
        w /= 64.0  # convert from subpixels
        h /= 64.0
        d = font.get_descent()
        d /= 64.0
        return w, h, d
