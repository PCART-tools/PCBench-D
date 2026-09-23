    @property
    def content_type(self):
        """Content type"""
        if self._content_type is not None:
            return self._content_type
        elif self._filename is not None:
            mime = mimetypes.guess_type(self._filename)[0]
            return 'application/octet-stream' if mime is None else mime
        else:
            return Payload._content_type
