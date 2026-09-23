    @property
    def content_length(self, *, _CONTENT_LENGTH=hdrs.CONTENT_LENGTH):
        """The value of Content-Length HTTP header."""
        l = self._headers.get(_CONTENT_LENGTH)
        if l is None:
            return None
        else:
            return int(l)
