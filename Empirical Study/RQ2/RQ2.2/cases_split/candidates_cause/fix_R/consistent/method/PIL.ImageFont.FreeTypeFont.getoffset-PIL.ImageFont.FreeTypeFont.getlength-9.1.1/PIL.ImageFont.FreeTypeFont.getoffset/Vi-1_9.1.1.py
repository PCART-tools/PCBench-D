    def getoffset(self, text):
        """
        Returns the offset of given text. This is the gap between the
        starting coordinate and the first marking. Note that this gap is
        included in the result of :py:func:`~PIL.ImageFont.FreeTypeFont.getsize`.

        :param text: Text to measure.

        :return: A tuple of the x and y offset
        """
        return self.font.getsize(text)[1]
