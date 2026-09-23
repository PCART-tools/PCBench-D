    def _get_font(self, prop):
        fname = fm.findfont(prop)
        font = fm.get_font(fname)
        font.clear()
        size = prop.get_size_in_points()
        font.set_size(size, 72.0)
        return font
