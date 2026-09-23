    def textbbox(self, xy, text, font):
        """
        Returns bounding box (in pixels) of given text.

        :return: ``(left, top, right, bottom)`` bounding box

        .. seealso:: :py:meth:`PIL.ImageDraw.ImageDraw.textbbox`
        """
        if self.transform:
            xy = ImagePath.Path(xy)
            xy.transform(self.transform)
        return self.draw.textbbox(xy, text, font=font.font)
