    def textbbox(
        self, xy: tuple[float, float], text: AnyStr, font: Font
    ) -> tuple[float, float, float, float]:
        """
        Returns bounding box (in pixels) of given text.

        :return: ``(left, top, right, bottom)`` bounding box

        .. seealso:: :py:meth:`PIL.ImageDraw.ImageDraw.textbbox`
        """
        if self.transform:
            path = ImagePath.Path(xy)
            path.transform(self.transform)
            xy = path
        return self.draw.textbbox(xy, text, font=font.font)
