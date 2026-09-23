    def text(self, xy: tuple[float, float], text: AnyStr, font: Font) -> None:
        """
        Draws the string at the given position.

        .. seealso:: :py:meth:`PIL.ImageDraw.ImageDraw.text`
        """
        if self.transform:
            path = ImagePath.Path(xy)
            path.transform(self.transform)
            xy = path
        self.draw.text(xy, text, font=font.font, fill=font.color)
