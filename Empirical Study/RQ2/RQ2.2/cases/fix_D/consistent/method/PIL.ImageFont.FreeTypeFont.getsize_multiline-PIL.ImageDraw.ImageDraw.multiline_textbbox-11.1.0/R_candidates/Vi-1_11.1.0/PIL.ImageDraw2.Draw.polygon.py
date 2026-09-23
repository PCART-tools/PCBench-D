    def polygon(self, xy: Coords, pen: Pen | Brush | None, *options: Any) -> None:
        """
        Draws a polygon.

        The polygon outline consists of straight lines between the given
        coordinates, plus a straight line between the last and the first
        coordinate.


        .. seealso:: :py:meth:`PIL.ImageDraw.ImageDraw.polygon`
        """
        self.render("polygon", xy, pen, *options)
