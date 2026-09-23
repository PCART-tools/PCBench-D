    def chord(self, xy, start, end, *options):
        """
        Same as :py:meth:`~PIL.ImageDraw2.Draw.arc`, but connects the end points
        with a straight line.

        .. seealso:: :py:meth:`PIL.ImageDraw.ImageDraw.chord`
        """
        self.render("chord", xy, start, end, *options)
