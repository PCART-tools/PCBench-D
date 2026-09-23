    def points_to_pixels(self, points):
        # docstring inherited
        return points * (PIXELS_PER_INCH / 72.0 * self.dpi / 72.0)
