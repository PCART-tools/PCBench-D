    def text(self, xy, text, font):
        """
        Draws the string at the given position.

        .. seealso:: :py:meth:`PIL.ImageDraw.ImageDraw.text`
        """
        if self.transform:
            xy = ImagePath.Path(xy)
            xy.transform(self.transform)
        self.draw.text(xy, text, font=font.font, fill=font.color)
