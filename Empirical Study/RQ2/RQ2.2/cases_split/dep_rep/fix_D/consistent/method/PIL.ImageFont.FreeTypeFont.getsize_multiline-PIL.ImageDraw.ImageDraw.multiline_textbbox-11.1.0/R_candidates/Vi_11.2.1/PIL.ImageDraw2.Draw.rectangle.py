    def rectangle(self, xy: Coords, pen: Pen | Brush | None, *options: Any) -> None:
        """
        Draws a rectangle.

        .. seealso:: :py:meth:`PIL.ImageDraw.ImageDraw.rectangle`
        """
        self.render("rectangle", xy, pen, *options)
