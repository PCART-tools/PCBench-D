    def getlength(
        self, text: str | bytes | bytearray, *args: Any, **kwargs: Any
    ) -> int:
        """
        Returns length (in pixels) of given text.
        This is the amount by which following text should be offset.

        .. versionadded:: 9.2.0
        """
        _string_length_check(text)
        width, height = self.font.getsize(text)
        return width
