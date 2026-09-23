    @content_length.setter
    def content_length(self, value):
        if value is not None:
            value = int(value)
            # TODO: raise error if chunked enabled
            self._headers[hdrs.CONTENT_LENGTH] = str(value)
        else:
            self._headers.pop(hdrs.CONTENT_LENGTH, None)
