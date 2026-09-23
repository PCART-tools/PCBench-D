class Response(HttpMessage):
    """Create http response message.

    Transport is a socket stream transport. status is a response status code,
    status has to be integer value. http_version is a tuple that represents
    http version, (1, 0) stands for HTTP/1.0 and (1, 1) is for HTTP/1.1
    """

    HOP_HEADERS = {
        'CONNECTION',
        'KEEP-ALIVE',
        'PROXY-AUTHENTICATE',
        'PROXY-AUTHORIZATION',
        'TE',
        'TRAILERS',
        'TRANSFER-ENCODING',
        'UPGRADE',
        'SERVER',
        'DATE',
    }

    def __init__(self, transport, status, http_version=(1, 1), close=False):
        super().__init__(transport, http_version, close)

        self.status = status
        self.status_line = 'HTTP/{}.{} {} {}\r\n'.format(
            http_version[0], http_version[1], status,
            RESPONSES.get(status, (status,))[0])

    def _add_default_headers(self):
        super()._add_default_headers()
        self.headers.extend((('DATE', format_date_time(None)),
                             ('SERVER', self.SERVER_SOFTWARE),))
