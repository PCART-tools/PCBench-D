    def regular_polygon(
        self,
        bounding_circle: Sequence[Sequence[float] | float],
        n_sides: int,
        rotation: float = 0,
        fill: _Ink | None = None,
        outline: _Ink | None = None,
        width: int = 1,
    ) -> None:
        """Draw a regular polygon."""
        xy = _compute_regular_polygon_vertices(bounding_circle, n_sides, rotation)
        self.polygon(xy, fill, outline, width)
