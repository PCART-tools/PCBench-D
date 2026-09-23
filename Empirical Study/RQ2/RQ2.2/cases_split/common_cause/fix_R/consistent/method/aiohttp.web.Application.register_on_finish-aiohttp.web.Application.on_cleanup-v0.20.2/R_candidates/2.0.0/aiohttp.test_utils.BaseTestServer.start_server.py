    @asyncio.coroutine
    def start_server(self, loop=None, **kwargs):
        if self.server:
            return
        self._loop = loop
        self.port = unused_port()
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
            handler, self.host, self.port, ssl=self._ssl)
