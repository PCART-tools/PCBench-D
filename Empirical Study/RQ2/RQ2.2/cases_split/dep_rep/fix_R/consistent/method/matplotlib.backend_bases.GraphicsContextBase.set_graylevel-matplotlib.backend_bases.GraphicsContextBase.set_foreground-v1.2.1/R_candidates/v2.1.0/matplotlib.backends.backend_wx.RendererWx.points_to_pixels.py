    def points_to_pixels(self, points):
        """
        convert point measures to pixes using dpi and the pixels per
        inch of the display
        """
        return points * (PIXELS_PER_INCH / 72.0 * self.dpi / 72.0)
