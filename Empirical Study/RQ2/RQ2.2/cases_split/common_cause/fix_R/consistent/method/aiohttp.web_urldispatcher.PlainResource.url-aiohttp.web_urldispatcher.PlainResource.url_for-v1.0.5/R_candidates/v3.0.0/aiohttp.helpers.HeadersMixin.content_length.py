    @property
    def content_length(self, *, _CONTENT_LENGTH=hdrs.CONTENT_LENGTH):
        """The value of Content-Length HTTP header."""
        content_length = self._headers.get(_CONTENT_LENGTH)

        if content_length:
            return int(content_length)
