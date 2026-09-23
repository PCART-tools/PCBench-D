    def ellipse(self, xy, *options):
        """
        Draws an ellipse inside the given bounding box.

        .. seealso:: :py:meth:`PIL.ImageDraw.ImageDraw.ellipse`
        """
        self.render("ellipse", xy, *options)
