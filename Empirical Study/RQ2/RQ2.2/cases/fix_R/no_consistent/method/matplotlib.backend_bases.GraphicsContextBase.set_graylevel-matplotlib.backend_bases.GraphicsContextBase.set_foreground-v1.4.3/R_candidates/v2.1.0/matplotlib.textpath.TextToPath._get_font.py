    def _get_font(self, prop):
        """
        find a ttf font.
        """
        fname = font_manager.findfont(prop)
        font = get_font(fname)
        font.set_size(self.FONT_SCALE, self.DPI)

        return font
