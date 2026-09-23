    def _get_scale(self, renderer):
        unit = self.get_unit()
        if unit == "pixels":
            return 1.
        else:
            return renderer.points_to_pixels(1.)
