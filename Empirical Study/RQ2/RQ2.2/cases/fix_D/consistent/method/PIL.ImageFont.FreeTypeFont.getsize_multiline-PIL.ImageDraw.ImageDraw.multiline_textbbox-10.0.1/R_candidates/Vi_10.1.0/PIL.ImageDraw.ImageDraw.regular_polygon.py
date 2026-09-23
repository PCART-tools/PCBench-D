    def regular_polygon(
        self, bounding_circle, n_sides, rotation=0, fill=None, outline=None, width=1
    ):
        """Draw a regular polygon."""
        xy = _compute_regular_polygon_vertices(bounding_circle, n_sides, rotation)
        self.polygon(xy, fill, outline, width)
