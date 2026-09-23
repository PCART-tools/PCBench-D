    @text.setter
    def text(self, text):
        if text is not None and not isinstance(text, str):
            raise TypeError("text argument must be str (%r)" % type(text))

        if self.content_type == 'application/octet-stream':
            self.content_type = 'text/plain'
        if self.charset is None:
            self.charset = 'utf-8'

        self.body = text.encode(self.charset)
