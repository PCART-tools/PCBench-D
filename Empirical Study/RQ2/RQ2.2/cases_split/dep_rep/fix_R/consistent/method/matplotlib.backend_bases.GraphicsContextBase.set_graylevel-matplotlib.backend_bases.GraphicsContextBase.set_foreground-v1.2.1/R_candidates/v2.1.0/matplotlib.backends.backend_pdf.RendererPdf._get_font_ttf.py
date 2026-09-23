    def _get_font_ttf(self, prop):
        filename = findfont(prop)
        font = get_font(filename)
        font.clear()
        font.set_size(prop.get_size_in_points(), 72)
        return font
