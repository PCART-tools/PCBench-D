    @content_length.setter
    def content_length(self, value):
        if value is not None:
            value = int(value)
            if self._chunked:
                raise RuntimeError("You can't set content length when "
                                   "chunked encoding is enable")
            self._headers[hdrs.CONTENT_LENGTH] = str(value)
        else:
            self._headers.pop(hdrs.CONTENT_LENGTH, None)
