    @text.setter
    def text(self, text):
        assert text is None or isinstance(text, str), \
            "text argument must be str (%r)" % type(text)

        if self.content_type == 'application/octet-stream':
            self.content_type = 'text/plain'
        if self.charset is None:
            self.charset = 'utf-8'

        self._body = text.encode(self.charset)
        self._body_payload = False
