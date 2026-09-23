    @property
    def content_type(self, *, _CONTENT_TYPE=hdrs.CONTENT_TYPE):
        """The value of content part for Content-Type HTTP header."""
        raw = self._headers.get(_CONTENT_TYPE)
        if self._stored_content_type != raw:
            self._parse_content_type(raw)
        return self._content_type
