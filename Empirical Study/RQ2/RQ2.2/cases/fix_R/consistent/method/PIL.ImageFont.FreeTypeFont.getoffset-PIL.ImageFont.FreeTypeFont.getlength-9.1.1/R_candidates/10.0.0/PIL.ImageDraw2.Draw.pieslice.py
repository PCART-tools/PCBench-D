    def pieslice(self, xy, start, end, *options):
        """
        Same as arc, but also draws straight lines between the end points and the
        center of the bounding box.

        .. seealso:: :py:meth:`PIL.ImageDraw.ImageDraw.pieslice`
        """
        self.render("pieslice", xy, start, end, *options)
