    @asyncio.coroutine
    def start_server(self, **kwargs):
        if self.server:
            return
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
        yield from self.app.startup()
        self.handler = self.app.make_handler(**kwargs)
        self.server = yield from self._loop.create_server(self.handler,
                                                          self.host,
                                                          self.port,
                                                          ssl=self._ssl)
