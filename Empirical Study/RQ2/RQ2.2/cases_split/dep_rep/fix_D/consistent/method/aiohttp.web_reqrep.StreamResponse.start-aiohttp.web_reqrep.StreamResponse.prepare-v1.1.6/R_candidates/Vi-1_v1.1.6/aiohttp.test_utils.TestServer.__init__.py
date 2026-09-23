    def __init__(self, app, *, scheme=sentinel, host='127.0.0.1'):
        self.app = app
        self._loop = app.loop
        self.port = None
        self.server = None
        self.handler = None
        self._root = None
        self.host = host
        self._closed = False
        self.scheme = scheme
