    def get_text_width_height_descent(self, s, prop, ismath):
        if rcParams['text.usetex']:
            texmanager = self.get_texmanager()
            fontsize = prop.get_size_in_points()
            w, h, d = texmanager.get_text_width_height_descent(s, fontsize,
                                                               renderer=self)
            return w, h, d

        if ismath:
            w, h, d, glyphs, rects, used_characters = \
                self.mathtext_parser.parse(s, 72, prop)

        elif rcParams['pdf.use14corefonts']:
            font = self._get_font_afm(prop)
            l, b, w, h, d = font.get_str_bbox_and_descent(s)
            scale = prop.get_size_in_points()
            w *= scale / 1000
            h *= scale / 1000
            d *= scale / 1000
        else:
            font = self._get_font_ttf(prop)
            font.set_text(s, 0.0, flags=LOAD_NO_HINTING)
            w, h = font.get_width_height()
            scale = (1.0 / 64.0)
            w *= scale
            h *= scale
            d = font.get_descent()
            d *= scale
        return w, h, d
