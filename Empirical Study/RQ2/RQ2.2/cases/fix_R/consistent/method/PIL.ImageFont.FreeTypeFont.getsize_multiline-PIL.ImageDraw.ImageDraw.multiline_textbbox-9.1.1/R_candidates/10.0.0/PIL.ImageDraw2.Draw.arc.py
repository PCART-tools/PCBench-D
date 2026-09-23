    def arc(self, xy, start, end, *options):
        """
        Draws an arc (a portion of a circle outline) between the start and end
        angles, inside the given bounding box.

        .. seealso:: :py:meth:`PIL.ImageDraw.ImageDraw.arc`
        """
        self.render("arc", xy, start, end, *options)
