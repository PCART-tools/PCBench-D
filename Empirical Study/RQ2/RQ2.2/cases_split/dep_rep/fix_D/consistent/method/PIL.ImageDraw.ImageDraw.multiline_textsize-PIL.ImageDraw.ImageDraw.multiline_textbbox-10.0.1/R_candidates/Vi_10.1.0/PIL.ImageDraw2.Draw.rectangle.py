    def rectangle(self, xy, *options):
        """
        Draws a rectangle.

        .. seealso:: :py:meth:`PIL.ImageDraw.ImageDraw.rectangle`
        """
        self.render("rectangle", xy, *options)
