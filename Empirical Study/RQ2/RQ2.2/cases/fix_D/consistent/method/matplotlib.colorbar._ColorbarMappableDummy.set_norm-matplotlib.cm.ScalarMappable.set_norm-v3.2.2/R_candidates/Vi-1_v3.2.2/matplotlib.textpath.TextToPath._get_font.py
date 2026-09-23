    def _get_font(self, prop):
        """
        Find the `FT2Font` matching font properties *prop*, with its size set.
        """
        fname = font_manager.findfont(prop)
        font = get_font(fname)
        font.set_size(self.FONT_SCALE, self.DPI)
        return font
