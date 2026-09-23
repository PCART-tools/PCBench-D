    def textlength(self, text: AnyStr, font: Font) -> float:
        """
        Returns length (in pixels) of given text.
        This is the amount by which following text should be offset.

        .. seealso:: :py:meth:`PIL.ImageDraw.ImageDraw.textlength`
        """
        return self.draw.textlength(text, font=font.font)
