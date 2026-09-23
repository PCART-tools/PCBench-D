class UnixConnector(BaseConnector):

    def __init__(self, path, *args, **kw):
        super().__init__(*args, **kw)

        self.path = path

    @asyncio.coroutine
    def _create_connection(self, req, **kwargs):
        return (yield from self._loop.create_unix_connection(
            self._factory, self.path, **kwargs))
