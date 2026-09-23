    def get_bbox(self, renderer):
        dpi_cor = renderer.points_to_pixels(1.) if self._dpi_cor else 1.
        zoom = self.get_zoom()
        data = self.get_data()
        ny, nx = data.shape[:2]
        w, h = dpi_cor * nx * zoom, dpi_cor * ny * zoom
        return Bbox.from_bounds(0, 0, w, h)
