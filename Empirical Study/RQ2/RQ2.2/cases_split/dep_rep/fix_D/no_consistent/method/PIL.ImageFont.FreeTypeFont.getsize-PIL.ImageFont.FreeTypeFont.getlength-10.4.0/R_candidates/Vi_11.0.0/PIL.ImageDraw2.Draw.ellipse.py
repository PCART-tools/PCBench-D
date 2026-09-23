    def ellipse(self, xy: Coords, pen: Pen | Brush | None, *options: Any) -> None:
        """
        Draws an ellipse inside the given bounding box.

        .. seealso:: :py:meth:`PIL.ImageDraw.ImageDraw.ellipse`
        """
        self.render("ellipse", xy, pen, *options)
