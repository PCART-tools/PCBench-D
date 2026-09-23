    def _get_agg_font(self, prop):
        """
        Get the font for text instance t, caching for efficiency
        """
        fname = findfont(prop)
        font = get_font(fname)

        font.clear()
        size = prop.get_size_in_points()
        font.set_size(size, self.dpi)

        return font
