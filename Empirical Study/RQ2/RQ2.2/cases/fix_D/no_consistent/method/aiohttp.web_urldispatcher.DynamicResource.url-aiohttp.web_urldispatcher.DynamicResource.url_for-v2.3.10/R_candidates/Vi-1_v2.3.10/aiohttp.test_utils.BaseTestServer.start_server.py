    @asyncio.coroutine
    def start_server(self, loop=None, **kwargs):
        if self.server:
            return
        self._loop = loop
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((self.host, 0))
        self.port = self._socket.getsockname()[1]
        self._ssl = kwargs.pop('ssl', None)
        if self.scheme is sentinel:
            if self._ssl:
                scheme = 'https'
            else:
                scheme = 'http'
            self.scheme = scheme
        self._root = URL('{}://{}:{}'.format(self.scheme,
                                             self.host,
                                             self.port))

        handler = yield from self._make_factory(**kwargs)
        self.server = yield from self._loop.create_server(
            handler, ssl=self._ssl, sock=self._socket)
