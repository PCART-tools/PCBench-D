    @_api.rename_parameter("3.4", "facename", "font")
    def render_glyph(self, ox, oy, font, font_class, sym, fontsize, dpi):
        """
        At position (*ox*, *oy*), draw the glyph specified by the remaining
        parameters (see `get_metrics` for their detailed description).
        """
        info = self._get_info(font, font_class, sym, fontsize, dpi)
        self.used_characters.setdefault(info.font.fname, set()).add(info.num)
        self.mathtext_backend.render_glyph(ox, oy, info)
