    async def start_server(self, loop=None, **kwargs):
        if self.runner:
            return
        self._loop = loop
        self._ssl = kwargs.pop('ssl', None)
        self.runner = await self._make_runner(**kwargs)
        await self.runner.setup()
        if not self.port:
            self.port = unused_port()
        site = TCPSite(self.runner, host=self.host, port=self.port,
                       ssl_context=self._ssl)
        await site.start()
        if self.scheme is sentinel:
            if self._ssl:
                scheme = 'https'
            else:
                scheme = 'http'
            self.scheme = scheme
        self._root = URL('{}://{}:{}'.format(self.scheme,
                                             self.host,
                                             self.port))
