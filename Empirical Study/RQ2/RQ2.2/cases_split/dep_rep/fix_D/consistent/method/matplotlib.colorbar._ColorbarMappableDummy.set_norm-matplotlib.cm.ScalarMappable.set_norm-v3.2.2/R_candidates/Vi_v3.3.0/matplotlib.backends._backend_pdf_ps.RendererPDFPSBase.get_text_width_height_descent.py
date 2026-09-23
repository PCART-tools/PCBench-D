    def get_text_width_height_descent(self, s, prop, ismath):
        # docstring inherited
        if ismath == "TeX":
            texmanager = self.get_texmanager()
            fontsize = prop.get_size_in_points()
            w, h, d = texmanager.get_text_width_height_descent(
                s, fontsize, renderer=self)
            return w, h, d
        elif ismath:
            parse = self.mathtext_parser.parse(s, 72, prop)
            return parse.width, parse.height, parse.depth
        elif mpl.rcParams[self._use_afm_rc_name]:
            font = self._get_font_afm(prop)
            l, b, w, h, d = font.get_str_bbox_and_descent(s)
            scale = prop.get_size_in_points() / 1000
            w *= scale
            h *= scale
            d *= scale
            return w, h, d
        else:
            font = self._get_font_ttf(prop)
            font.set_text(s, 0.0, flags=ft2font.LOAD_NO_HINTING)
            w, h = font.get_width_height()
            d = font.get_descent()
            scale = 1 / 64
            w *= scale
            h *= scale
            d *= scale
            return w, h, d
