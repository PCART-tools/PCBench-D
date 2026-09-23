    def line(self, xy: Coords, pen: Pen | Brush | None, *options: Any) -> None:
        """
        Draws a line between the coordinates in the ``xy`` list.

        .. seealso:: :py:meth:`PIL.ImageDraw.ImageDraw.line`
        """
        self.render("line", xy, pen, *options)
