    def _draw_polygon(self):
        """Redraw the polygon based on the new vertex positions."""
        self._draw_polygon_without_update()
        self.update()
