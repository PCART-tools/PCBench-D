    def __init__(self, *, scheme=sentinel, loop=None,
                 host='127.0.0.1', skip_url_asserts=False, **kwargs):
        self._loop = loop
        self.port = None
        self.server = None
        self.handler = None
        self._root = None
        self.host = host
        self._closed = False
        self.scheme = scheme
        self.skip_url_asserts = skip_url_asserts
