    def getbbox(
        self, text: str | bytes | bytearray, *args: Any, **kwargs: Any
    ) -> tuple[int, int, int, int]:
        """
        Returns bounding box (in pixels) of given text.

        .. versionadded:: 9.2.0

        :param text: Text to render.

        :return: ``(left, top, right, bottom)`` bounding box
        """
        _string_length_check(text)
        width, height = self.font.getsize(text)
        return 0, 0, width, height
