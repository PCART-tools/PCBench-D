    def _get_font_ttf(self, prop):
        fname = findfont(prop)
        font = get_font(fname)
        font.clear()
        size = prop.get_size_in_points()
        font.set_size(size, 72.0)
        return font
