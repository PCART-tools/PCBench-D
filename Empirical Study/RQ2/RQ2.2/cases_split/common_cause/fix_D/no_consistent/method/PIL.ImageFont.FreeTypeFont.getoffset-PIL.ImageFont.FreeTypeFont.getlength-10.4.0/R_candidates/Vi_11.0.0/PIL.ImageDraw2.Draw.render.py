    def render(
        self,
        op: str,
        xy: Coords,
        pen: Pen | Brush | None,
        brush: Brush | Pen | None = None,
        **kwargs: Any,
    ) -> None:
        # handle color arguments
        outline = fill = None
        width = 1
        if isinstance(pen, Pen):
            outline = pen.color
            width = pen.width
        elif isinstance(brush, Pen):
            outline = brush.color
            width = brush.width
        if isinstance(brush, Brush):
            fill = brush.color
        elif isinstance(pen, Brush):
            fill = pen.color
        # handle transformation
        if self.transform:
            path = ImagePath.Path(xy)
            path.transform(self.transform)
            xy = path
        # render the item
        if op in ("arc", "line"):
            kwargs.setdefault("fill", outline)
        else:
            kwargs.setdefault("fill", fill)
            kwargs.setdefault("outline", outline)
        if op == "line":
            kwargs.setdefault("width", width)
        getattr(self.draw, op)(xy, **kwargs)
