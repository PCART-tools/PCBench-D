    def arc(
        self,
        xy: Coords,
        pen: Pen | Brush | None,
        start: float,
        end: float,
        *options: Any,
    ) -> None:
        """
        Draws an arc (a portion of a circle outline) between the start and end
        angles, inside the given bounding box.

        .. seealso:: :py:meth:`PIL.ImageDraw.ImageDraw.arc`
        """
        self.render("arc", xy, pen, *options, start=start, end=end)
