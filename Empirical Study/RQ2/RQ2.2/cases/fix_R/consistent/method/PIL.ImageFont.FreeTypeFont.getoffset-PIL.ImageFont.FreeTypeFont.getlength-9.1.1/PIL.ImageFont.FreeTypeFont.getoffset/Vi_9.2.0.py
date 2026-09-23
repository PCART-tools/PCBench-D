    def getoffset(self, text):
        """
        .. deprecated:: 9.2.0

        Use :py:meth:`.getbbox` instead.

        Returns the offset of given text. This is the gap between the
        starting coordinate and the first marking. Note that this gap is
        included in the result of :py:func:`~PIL.ImageFont.FreeTypeFont.getsize`.

        :param text: Text to measure.

        :return: A tuple of the x and y offset
        """
        deprecate("getoffset", 10, "getbbox")
        return self.font.getsize(text)[1]
