class Request(HttpMessage):

    HOP_HEADERS = ()

    def __init__(self, transport, method, path,
                 http_version=(1, 1), close=False):
        super().__init__(transport, http_version, close)

        self.method = method
        self.path = path
        self.status_line = '{0} {1} HTTP/{2[0]}.{2[1]}\r\n'.format(
            method, path, http_version)

    def _add_default_headers(self):
        super()._add_default_headers()

        if not self._has_user_agent:
            self.headers['USER-AGENT'] = self.SERVER_SOFTWARE
