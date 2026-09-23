    @body.setter
    def body(self, body):
        if body is not None and not isinstance(body, bytes):
            raise TypeError("body argument must be bytes (%r)" % type(body))
        self._body = body
        if body is not None:
            self.content_length = len(body)
        else:
            self.content_length = 0
