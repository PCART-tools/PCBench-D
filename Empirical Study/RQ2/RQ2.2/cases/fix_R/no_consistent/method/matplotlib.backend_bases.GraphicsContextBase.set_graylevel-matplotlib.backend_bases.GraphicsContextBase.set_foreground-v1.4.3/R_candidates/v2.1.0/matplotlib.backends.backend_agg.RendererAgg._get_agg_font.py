    def _get_agg_font(self, prop):
        """
        Get the font for text instance t, cacheing for efficiency
        """
        fname = findfont(prop)
        font = get_font(
            fname,
            hinting_factor=rcParams['text.hinting_factor'])

        font.clear()
        size = prop.get_size_in_points()
        font.set_size(size, self.dpi)

        return font
