    def _get_font_ttf(self, prop):
        fname = font_manager.findfont(prop)
        font = font_manager.get_font(fname)
        font.clear()
        font.set_size(prop.get_size_in_points(), 72)
        return font
