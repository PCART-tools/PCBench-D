    def render_glyph(self, ox, oy, facename, font_class, sym, fontsize, dpi):
        """
        Draw a glyph at

          - *ox*, *oy*: position

          - *facename*: One of the TeX face names

          - *font_class*:

          - *sym*: TeX symbol name or single character

          - *fontsize*: fontsize in points

          - *dpi*: The dpi to draw at.
        """
        info = self._get_info(facename, font_class, sym, fontsize, dpi)
        realpath, stat_key = get_realpath_and_stat(info.font.fname)
        used_characters = self.used_characters.setdefault(
            stat_key, (realpath, set()))
        used_characters[1].add(info.num)
        self.mathtext_backend.render_glyph(ox, oy, info)
