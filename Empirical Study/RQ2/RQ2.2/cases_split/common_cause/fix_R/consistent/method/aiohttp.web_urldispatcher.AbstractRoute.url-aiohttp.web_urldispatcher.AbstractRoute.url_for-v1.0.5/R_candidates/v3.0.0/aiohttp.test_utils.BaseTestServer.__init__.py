    def __init__(self, *, scheme=sentinel, loop=None,
                 host='127.0.0.1', port=None, skip_url_asserts=False,
                 **kwargs):
        self._loop = loop
        self.runner = None
        self._root = None
        self.host = host
        self.port = port
        self._closed = False
        self.scheme = scheme
        self.skip_url_asserts = skip_url_asserts
