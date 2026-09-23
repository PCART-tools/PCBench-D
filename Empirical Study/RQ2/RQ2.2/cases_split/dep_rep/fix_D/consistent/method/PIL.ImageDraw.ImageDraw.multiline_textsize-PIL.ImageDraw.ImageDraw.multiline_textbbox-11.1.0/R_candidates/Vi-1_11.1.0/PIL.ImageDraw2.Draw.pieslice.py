    def pieslice(
        self,
        xy: Coords,
        pen: Pen | Brush | None,
        start: float,
        end: float,
        *options: Any,
    ) -> None:
        """
        Same as arc, but also draws straight lines between the end points and the
        center of the bounding box.

        .. seealso:: :py:meth:`PIL.ImageDraw.ImageDraw.pieslice`
        """
        self.render("pieslice", xy, pen, *options, start=start, end=end)
