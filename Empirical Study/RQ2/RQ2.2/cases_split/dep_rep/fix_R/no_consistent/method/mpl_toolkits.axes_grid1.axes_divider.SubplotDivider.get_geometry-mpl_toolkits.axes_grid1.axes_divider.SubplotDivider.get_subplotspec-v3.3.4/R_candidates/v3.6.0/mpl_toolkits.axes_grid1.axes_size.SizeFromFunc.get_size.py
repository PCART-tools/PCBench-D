    def get_size(self, renderer):
        rel_size = 0.

        bb = self._func(renderer)
        dpi = renderer.points_to_pixels(72.)
        abs_size = bb/dpi

        return rel_size, abs_size
