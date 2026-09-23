    def get_bbox(self, renderer):
        # docstring inherited
        dpi_cor = renderer.points_to_pixels(1.)
        return Bbox.from_bounds(
            -self.xdescent * dpi_cor, -self.ydescent * dpi_cor,
            self.width * dpi_cor, self.height * dpi_cor)
