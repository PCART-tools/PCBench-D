    def render(self, op, xy, pen, brush=None):
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
            xy = ImagePath.Path(xy)
            xy.transform(self.transform)
        # render the item
        if op == "line":
            self.draw.line(xy, fill=outline, width=width)
        else:
            getattr(self.draw, op)(xy, fill=fill, outline=outline)
