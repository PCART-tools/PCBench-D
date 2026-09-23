    def chord(
        self,
        xy: Coords,
        pen: Pen | Brush | None,
        start: float,
        end: float,
        *options: Any,
    ) -> None:
        """
        Same as :py:meth:`~PIL.ImageDraw2.Draw.arc`, but connects the end points
        with a straight line.

        .. seealso:: :py:meth:`PIL.ImageDraw.ImageDraw.chord`
        """
        self.render("chord", xy, pen, *options, start=start, end=end)
