    def __init__(self, value, *, headers=None,
                 content_type=sentinel, filename=None, encoding=None):
        self._value = value
        self._encoding = encoding
        self._filename = filename
        if headers is not None:
            self._headers = CIMultiDict(headers)
            if content_type is sentinel and hdrs.CONTENT_TYPE in self._headers:
                content_type = self._headers[hdrs.CONTENT_TYPE]

        if content_type is sentinel:
            content_type = None

        self._content_type = content_type
