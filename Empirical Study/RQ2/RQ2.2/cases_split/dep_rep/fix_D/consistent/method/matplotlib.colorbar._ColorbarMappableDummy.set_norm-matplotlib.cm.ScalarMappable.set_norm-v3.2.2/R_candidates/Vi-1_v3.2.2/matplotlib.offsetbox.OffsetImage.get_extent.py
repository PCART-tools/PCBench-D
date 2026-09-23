    def get_extent(self, renderer):
        if self._dpi_cor:  # True, do correction
            dpi_cor = renderer.points_to_pixels(1.)
        else:
            dpi_cor = 1.

        zoom = self.get_zoom()
        data = self.get_data()
        ny, nx = data.shape[:2]
        w, h = dpi_cor * nx * zoom, dpi_cor * ny * zoom

        return w, h, 0, 0
