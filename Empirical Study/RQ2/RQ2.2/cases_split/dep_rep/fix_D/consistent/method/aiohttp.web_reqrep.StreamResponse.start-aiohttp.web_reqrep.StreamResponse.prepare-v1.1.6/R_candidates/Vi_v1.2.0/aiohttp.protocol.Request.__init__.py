    def __init__(self, transport, method, path,
                 http_version=HttpVersion11, close=False):
        # set the default for HTTP 0.9 to be different
        # will only be overwritten with keep-alive header
        if http_version < HttpVersion10:
            close = True

        super().__init__(transport, http_version, close)

        self._method = method
        self._path = path
