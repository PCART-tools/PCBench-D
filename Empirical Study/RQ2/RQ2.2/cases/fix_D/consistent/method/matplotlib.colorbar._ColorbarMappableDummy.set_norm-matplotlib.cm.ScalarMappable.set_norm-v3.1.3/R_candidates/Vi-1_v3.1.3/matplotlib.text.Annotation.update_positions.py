    def update_positions(self, renderer):
        """Update the pixel positions of the annotated point and the text."""
        xy_pixel = self._get_position_xy(renderer)
        self._update_position_xytext(renderer, xy_pixel)
